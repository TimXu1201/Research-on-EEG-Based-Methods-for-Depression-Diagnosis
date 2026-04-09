import mne
import os
import numpy as np
import pandas as pd
from mne.preprocessing import ICA

def preprocess_eeg(input_path, output_path):
    try:
        # 1. Read CSV file
        df = pd.read_csv(input_path)
        data = df.values.T * 1e-6  # Convert to volts (assuming original data is in microvolts)
        ch_names = df.columns.tolist()
        
        info = mne.create_info(ch_names=ch_names, sfreq=1000, ch_types='eeg')
        raw = mne.io.RawArray(data, info)

        # 2. Set electrode positions
        montage = mne.channels.make_standard_montage('standard_1005')
        good_chs = [ch for ch in raw.ch_names if ch in montage.ch_names]
        raw.pick_channels(good_chs)
        raw.set_montage(montage)

        # 3. Select EEG channels
        raw.pick_types(meg=False, eeg=True)

        # 4. Resample
        raw.resample(250, npad='auto')

        # 5. Notch filter
        raw.notch_filter(np.arange(50, 125, 50), fir_design='firwin')

        # 6. Band-pass filter
        raw.filter(32, 45, fir_design='firwin')

        # 7. Bad channel detection
        data_matrix = raw.get_data()
        stds = np.std(data_matrix, axis=1)
        std_threshold = np.mean(stds) + 2 * np.std(stds)
        std_bads = [raw.ch_names[i] for i, std in enumerate(stds) if std > std_threshold]
        raw.info['bads'] = std_bads

        # 8. Bad channel interpolation
        raw.interpolate_bads(reset_bads=True)

        # 9. Epoching
        events = mne.make_fixed_length_events(raw, duration=2.0)
        epochs = mne.Epochs(
            raw,
            events,
            tmin=0,
            tmax=2.0,
            baseline=None,
            preload=True,
            reject_by_annotation=False
        )

        total_epochs = len(epochs)

        # 10. Reject bad epochs
        reject_criteria = dict(eeg=500e-6)
        epochs.drop_bad(reject=reject_criteria)
        kept_epochs = len(epochs)

        if kept_epochs == 0:
            raise RuntimeError("All epochs were dropped, skipping ICA.")

        # 11. Re-reference
        epochs.set_eeg_reference('average', projection=True)

        # 12. ICA
        ica = ICA(n_components=15, method='infomax', random_state=97)
        ica.fit(epochs)
        ica.apply(epochs)

        # 13. Save preprocessed data
        output_file = os.path.join(output_path, 'preprocessed-epo.fif')
        epochs.save(output_file, overwrite=True)

        return {
            "status": "success",
            "total_epochs": total_epochs,
            "kept_epochs": kept_epochs,
            "dropped_epochs": total_epochs - kept_epochs
        }

    except Exception as e:
        return {
            "status": "fail",
            "error": str(e),
            "total_epochs": 0,
            "kept_epochs": 0,
            "dropped_epochs": 0
        }

# Loop over all subjects and all session data
base_dir = r'E:\derivatives'
output_base = r'E:\preprocessed_data_low gamma'
summary = []

for sub in os.listdir(base_dir):
    sub_dir = os.path.join(base_dir, sub)
    if os.path.isdir(sub_dir):
        for ses in os.listdir(sub_dir):
            eeg_dir = os.path.join(sub_dir, ses, 'eeg')
            if os.path.isdir(eeg_dir):
                for fname in os.listdir(eeg_dir):
                    if fname.endswith('.csv'):
                        input_path = os.path.join(eeg_dir, fname)
                        output_path = os.path.join(output_base, sub, ses, 'eeg')
                        output_file = os.path.join(output_path, 'preprocessed-epo.fif')

                        # Skip if result already exists
                        if os.path.exists(output_file):
                            print(f"Skipped (already exists): {sub}/{ses}/{fname}")
                            summary.append((sub, ses, fname, "-", "-", "-", "Skipped"))
                            continue

                        os.makedirs(output_path, exist_ok=True)
                        result = preprocess_eeg(input_path, output_path)

                        if result["status"] == "success":
                            print(
                                f"Processed: {sub}/{ses}/{fname} | "
                                f"Total: {result['total_epochs']}, "
                                f"Kept: {result['kept_epochs']}, "
                                f"Dropped: {result['dropped_epochs']}"
                            )
                            summary.append(
                                (
                                    sub,
                                    ses,
                                    fname,
                                    result["total_epochs"],
                                    result["kept_epochs"],
                                    result["dropped_epochs"],
                                    "OK",
                                )
                            )
                        else:
                            print(f"Failed: {sub}/{ses}/{fname} | Error: {result['error']}")
                            summary.append((sub, ses, fname, 0, 0, 0, f"Error: {result['error']}"))

# Print summary
print("\nSummary:")
ok_count = 0
fail_count = 0
skip_count = 0
for sub, ses, fname, total, kept, dropped, status in summary:
    print(
        f"- {sub}/{ses}/{fname} | "
        f"Total: {total}, Kept: {kept}, Dropped: {dropped} | {status}"
    )
    if status == "OK":
        ok_count += 1
    elif status == "Skipped":
        skip_count += 1
    else:
        fail_count += 1

print(f"\nSuccessfully processed: {ok_count}")
print(f"Skipped (already processed): {skip_count}")
print(f"Failed: {fail_count}")
