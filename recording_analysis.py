import pandas as pd
import numpy as np

import soundfile as sf  
import base64
import io

import matplotlib.pyplot as plt

import pyperclip
    

def snr(data):
  singleChannel = data
  try:
    singleChannel = np.sum(data, axis=1)
  except:
    # was mono after all
    pass
    
  norm = singleChannel / (max(np.amax(singleChannel), -1 * np.amin(singleChannel)))
  a = np.asanyarray(norm)
  m = a.mean(0)
  sd = a.std(axis=0, ddof=0)
  return 20*np.log10(abs(np.where(sd == 0, 0, m/sd)))

data_filepath = "./recordings_output.csv"
test_participant_demos = {
    '82A73E' : {'gender':'female', 'age': 27, 'accent' : 'canadian', 'condition' : 'normal'},
    '0FE229' :  {'gender':'female', 'age': 27, 'accent' : 'canadian', 'condition' : 'talking'},
    '849492' :  {'gender':'female', 'age': 27, 'accent' : 'canadian', 'condition' : 'traffic'},
    '30CFEC' : {'gender':'female', 'age': 27, 'accent' : 'canadian', 'condition' : 'normal'},
    'A0D4A2' :  {'gender':'female', 'age': 27, 'accent' : 'canadian', 'condition' : 'talking'},
    '740E61' :  {'gender':'female', 'age': 27, 'accent' : 'canadian', 'condition' : 'traffic'},
    '6E178B' : {'gender':'female', 'age': 26, 'accent' : 'canadian', 'condition' : 'normal'},
    'B3602E' :  {'gender':'female', 'age': 26, 'accent' : 'canadian', 'condition' : 'talking'},
    'ED5A02' :  {'gender':'female', 'age': 26, 'accent' : 'canadian', 'condition' : 'traffic'}
}

df = pd.read_csv(data_filepath)
print(df.head())
print(df.shape)

study_codes = df["study_code"].tolist()
audios = df['data'].tolist()

ages = [test_participant_demos[code]['age'] for code in study_codes]

audios = [base64.b64decode(bytearray.fromhex(a[2:]).decode()) for a in audios]
audio_data = [sf.read(io.BytesIO(a))[0] for a in audios]
snrs = [[snr(audio_data[i]), ages[i], test_participant_demos[study_codes[i]]['condition']] for i in range(len(audio_data))]
print(snrs[:5])

print(list(audio_data[0]))

# test_audio, tmp = sf.read('download.flac')
# print(snr(test_audio))


# PREPPING FOR PLOTS
normal_ages = [snr[1] for snr in snrs if snr[2] == 'normal']
normal_snrs = [snr[0] for snr in snrs if snr[2] == 'normal']

talking_ages = [snr[1] for snr in snrs if snr[2] == 'talking']
talking_snrs = [snr[0] for snr in snrs if snr[2] == 'talking']

traffic_ages = [snr[1] for snr in snrs if snr[2] == 'traffic']
traffic_snrs = [snr[0] for snr in snrs if snr[2] == 'traffic']

plt.plot(normal_ages, normal_snrs, 'o', color='black')
plt.plot(talking_ages, talking_snrs, 'o', color='red')
plt.plot(traffic_ages, traffic_snrs, 'o', color='blue')
# plt.show()

# plt.plot(df["fhir_patient_id"].tolist())

