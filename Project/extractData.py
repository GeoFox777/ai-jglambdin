import json
from json import JSONEncoder
import os
import math
import librosa

DATASET_PATH = "mini-genres" #path/to/marsyas/dataset
JSON_PATH = "data_10.json"
SAMPLE_RATE = 22050
TRACK_DURATION = 30 # measured in seconds (either make this variable or moderate my songs)
SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION

TEST_PATH = "mio"
TEST_JSON = "test.json"
LABEL_LIST = []

class JSON_data(JSONEncoder):
    def default(self, o):
        return o.__dict__

def save_mfcc(dataset_path, json_path, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=5):
    """Extracts MFCCs from music dataset and saves them into a json file along witgh genre labels.

        :param dataset_path (str): Path to dataset
        :param json_path (str): Path to json file used to save MFCCs
        :param num_mfcc (int): Number of coefficients to extract
        :param n_fft (int): Interval we consider to apply FFT. Measured in # of samples
        :param hop_length (int): Sliding window for FFT. Measured in # of samples
        :param: num_segments (int): Number of segments we want to divide sample tracks into
        :return:
        """

    # dictionary to store mapping, labels, and MFCCs
    data = {
        "mapping": [],
        "labels": [],
        "mfcc": [],
        "title": []
    }

    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

    # loop through all genre sub-folder
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

        # ensure we're processing a genre sub-folder level
        if dirpath is not dataset_path:

            # save genre label (i.e., sub-folder name) in the mapping
            semantic_label = dirpath.split("/")[-1]
            data["mapping"].append(semantic_label)
            LABEL_LIST.append(semantic_label)
            print("\nProcessing: {}".format(semantic_label))

            # process all audio files in genre sub-dir
            for f in filenames:

		# load audio file
                file_path = os.path.join(dirpath, f)
                signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)

                # if f[-7:-4] == "XxX":
                #     data["title"].append(f[0:-7])
                temp_f = f.split(".")
                data['title'].append(temp_f[0])


                # process all segments of audio file
                for d in range(num_segments):

                    # calculate start and finish sample for current segment
                    start = samples_per_segment * d
                    finish = start + samples_per_segment

                    # extract mfcc
                    mfcc = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
                    mfcc = mfcc.T

                    # store only mfcc feature with expected number of vectors
                    if len(mfcc) == num_mfcc_vectors_per_segment:
                        data["mfcc"].append(mfcc.tolist())
                        data["labels"].append(i-1)

                        temp_f = f.split(".")
                        data['title'].append(temp_f[0])

                        print("{}, segment:{}".format(file_path, d+1))
                        if f[-7:-4] == "XxX":
                            print()

                # for x in thisdict.values():
                #     if
                #     print(x)


    # save MFCCs to json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)

if __name__ == "__main__":
    save_mfcc(DATASET_PATH, JSON_PATH, num_segments=10)
    # save_mfcc(TEST_PATH, TEST_JSON, num_segments=10)


# def save_mfcc(dataset_path, json_path, test_path, test_json, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=5):
#     """Extracts MFCCs from music dataset and saves them into a json file along witgh genre labels.
#
#         :param dataset_path (str): Path to dataset
#         :param json_path (str): Path to json file used to save MFCCs
#         :param num_mfcc (int): Number of coefficients to extract
#         :param n_fft (int): Interval we consider to apply FFT. Measured in # of samples
#         :param hop_length (int): Sliding window for FFT. Measured in # of samples
#         :param: num_segments (int): Number of segments we want to divide sample tracks into
#         :return:
#         """
#
#     # dictionary to store mapping, labels, and MFCCs
#     data = {
#         "mapping": [],
#         "labels": [],
#         "mfcc": []
#     }
#
#     data1 = {
#         "mapping": [],
#         "labels": [],
#         "mfcc": []
#     }
#
#     samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
#     num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
#
#     # loop through all genre sub-folder
#     for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
#
#         # ensure we're processing a genre sub-folder level
#         if dirpath is not dataset_path:
#
#             # save genre label (i.e., sub-folder name) in the mapping
#             semantic_label = dirpath.split("/")[-1]
#             data["mapping"].append(semantic_label)
#             print("\nProcessing: {}".format(semantic_label))
#
#             # process all audio files in genre sub-dir
#             for f in filenames:
#
# 		# load audio file
#                 file_path = os.path.join(dirpath, f)
#                 signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)
#
#                 # process all segments of audio file
#                 for d in range(num_segments):
#
#                     # calculate start and finish sample for current segment
#                     start = samples_per_segment * d
#                     finish = start + samples_per_segment
#
#                     # extract mfcc
#                     mfcc = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
#                     mfcc = mfcc.T
#
#                     # store only mfcc feature with expected number of vectors
#                     if len(mfcc) == num_mfcc_vectors_per_segment:
#                         data["mfcc"].append(mfcc.tolist())
#                         data["labels"].append(i-1)
#                         print("{}, segment:{}".format(file_path, d+1))
#
#     # save MFCCs to json file
#     with open(json_path, "w") as fp:
#         JSON_data().encode(data)
#         json.dump(data, fp, indent=4)
#
#     for j, (dirpath, dirnames, filenames) in enumerate(os.walk(test_path)):
#
#         # ensure we're processing a genre sub-folder level
#         if dirpath is not test_path:
#             # save genre label (i.e., sub-folder name) in the mapping
#             semantic_label1 = dirpath.split("/")[-1]
#             data1["mapping"].append(semantic_label1)
#             print("\nProcessing: {}".format(semantic_label1))
#
#             # process all audio files in genre sub-dir
#             for f in filenames:
# 		        # load audio file
#                 test_path = os.path.join(dirpath, f)
#                 signal, sample_rate = librosa.load(test_path, sr=SAMPLE_RATE)
#
#                 # process all segments of audio file
#                 for d in range(num_segments):
#                     # calculate start and finish sample for current segment
#                     start = samples_per_segment * d
#                     finish = start + samples_per_segment
#
#                     # extract mfcc
#                     mfcc = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
#                     mfcc = mfcc.T
#
#                     # store only mfcc feature with expected number of vectors
#                     if len(mfcc) == num_mfcc_vectors_per_segment:
#                         data1["mfcc"].append(mfcc.tolist())
#                         data1["labels"].append(j-1)
#                         print("{}, segment:{}".format(file_path, d+1))
#
#     # save MFCCs to json file
#     with open(test_json, "w") as fp:
#         JSON_data().encode(data1)
#         json.dump(data1, fp, indent=4)
