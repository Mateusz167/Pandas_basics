# -*- coding: utf-8 -*-
"""Exercise: Creating, Reading and Writing

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/exercise-creating-reading-and-writing-07bfdef2-af13-4927-93a9-20e939f7f0e1.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240526/auto/storage/goog4_request%26X-Goog-Date%3D20240526T174123Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D00e8a2af0abb301e348142fa5422bc2559be86f9e8f9a9cc4fab0fb5fd55af7969006cf078b1ec8b942841dc56b17e6428203e919c41fbf9c0076829ee20069d8a46cac69b62fe4542186bda01a077622196068e9038001745da08f7a2000147a03f7abaf1b5c317566dc83e0f127171838b8783e2398e8da106464f514722bfb1de46b6785b19dbcd38814ff9aac63081e75df29990b6fe595c1f51b52e933b168724283ef455aa7931e86ec6c90e0eb1d2830b18916232bee83f6f95719ac6fdb348701bdb7b0cefbfdea2a3e5b6f3ff22203c4719b5c9c4c7eee2062e8aea046a43e9c0f043e246464df4e6af4c5803ba075cbeb3b9b0c96d9c034ddd9ca7
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'pitchfork-data:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F655%2F1252%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D6451f828b1730e72bbb649978b38efda374e76ed5d02a265c97e26df72fd3d32ff6a05cb0a60cfd4ccb049436564eba63a681a4900a5c5b1ea25d94d131067bebd31c8c87b90a10226512414db99beee4773cf4b2c602a436a073915f0be876f373d23d7f928bf9003976d8ba13f600c58bb1ee85694ec1a5c1e7859112bdbb06ed3e6fd3aaf2f7144c390565366b812785b9808b6f1feb7a115c7423d66d2dcf704f266a762720cf939faaf1909342758eb01794cd4f5998eca58282ce9562e483b6c3aed7dbf11b97a0f1b91710edd40e641d9966f9379e635152d622d0cf012223e5d822a804ff56ec9a0d2fdda1bbaab703f77f8fcf1032e5ec2c15fe579,chess:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F2321%2F3919%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D696d909ccfc618d1e1007db72f5bd2e41cb0c7e4b424d84a669c9ff3ccf22deef344b9162d14f5e7dca0dc8d681ce8052b5de98a6cd28600fc3c2ec1fbd0e97f24da55ef7b547dfa639d19dffc10a84f86a03dda3dc9c1b9d121952c93034bf0ffee2c927e4a4da9d8443fa5a282128378cb63b2b96278d98964c10623673d94249774c6c89b6282ef593054533501dad41e25a9a06b61c956e6c6aa9f177a32152447b7b29b36a1e4b558342737259e0bf00152a77801d3963f230fa6c343be5cb1d8ab354e8f687945e0831975c49f62614f97feb8e27dad6c0511ab9c9c82207d731ed02a8cfcdcef5f383fc145acf2c7052dec5b91d4598f8a57bc2806d6,kepler-exoplanet-search-results:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F2894%2F4877%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D693ff4961cd7786dbcd29a920d25d6029bb091c6417cf6197fec7b4719727871632621e42305a17f4f6231817b9dc530de6eca500c2985da6e7b296886edbc8c614a402f5f7d604b6c9c58528be4bed3982779c4326c336e51d7cd34aa09f7e97c2062d948d284408d456ac0365404b9132df6378346febd2397e678adaa799e448fb531c57aebb404cd0a94c611b3939389fe029fc614b23633021b486e44ac1d4c7f627e13ba8593d7f31e41b4466f5497f06b355c56c1ab4d402164b1c128e88ca2aeb3498f68df47809bb7dc498a6b874ac5daff807ec7111c92343dd7abb784236a581895afd2c031a4b31992b7ff1de4735d372bc998086ebae91351ea,things-on-reddit:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F3491%2F5624%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D8a39d29d1aebb3b8c4985f83ce30ff79b57609d794daa6f2da96199e572a669ccab922f07a425fc65ec208e3df8dad3dd0eb0a5aaf2d6cb51b52125aa4632d9cd748f07de24181850eb3cd5cc85df17b41ee2da68f3111579b0c1d175b8b53ca7f69643f625031708ad0427c327e817332d360c610c6338f3d6d09a2c69b3a171af2994ddee2825d5c09d978dac65e7c9182bda5d95f0022129063f84764f21c9b67629609eab580ab2950d64a958be94ae7ff0b2e5e2564cd69f791bd008a1c4b7e57fa5e256d567075a7943d339b5b973755f973386dc03df602c5a0f17d41541210a035f0061a03e3b91e79af00a64b3777873cf3213f3f8f4968d5be67d2,wine-reviews:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1442%2F8172%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D1eb72250f6e8abdcc0cf8e7c4e988bfa9e270cf9c908747bff01623285c39e06c7a4a35b8676205c13cc7c726e23b3b66fd07a0fd4b5d0d33592b6cb886809f0f12e03458d7239777b6ce29be26419ac2bd585b6459b4ce90721e50fa219198878d1bda41633af76bde537c30e0baf1cef3d745ca328b86955d70b6aee273b4061a0f193e951560b1c425f1996bee1f585661a8c28aa105ea4338fc13e9ffae0aeb7a4e8aec4d0d385ce5699fd7470e070509de5fbfbce5125d93c3c35e2bcb1f274e883bd05861edebd7f69af18508628d3e5829d012560419e734d6b86c9b93411a0d4c7373819d1a74f9a0cd6dd204baa3b2a2781fbf0edede2787987f796,ramen-ratings:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F9366%2F13206%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D2384ca97b2a2e95d4f33c078b83526f3e9de6e9ec21addfe1d8c8f7ecbd7613521011ab89035e77b492abe4871c0357b94057b97abbf4ba87aebb1d6adbe6ba65b9d86824c92b94d0a198514ec57d8f2fc6e958c82e6aaab1763f159a02bbc267db1f55d23167d80a71a5e064c88e7e96959154975c64fd18b72eff9df730074fbace00883fe45f757b66cd100036feb19931b1f5642e1e99cd9c78b097587d165d8bf9d4ff6e010c926d2146051900f40dab230e339cb693d6d21de4a4cd27f1e6114dddc202d41a449d0bea32eb253578a30747f8883146f0f3aa68c762ceed500e340d1e116eccdf8984692dae6686e60dcedc501b1e30aba8d8feb4f5ee7,powerlifting-database:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F179555%2F403916%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D4c7d51374ea9b6655737628b0bf96b48e7df9f62ea2e2f388dfa045d4a343a38ce7db9862af9cab729556b432c547447406d4780338b314bf38c170d56e0e076bb48a443a66b4b47f4873ed09de44746857c244851e39c978904c1b170c8edb4e439328b71b25fd815de37fe8d32e49a3acc3341559e94b6f370a2f5f8f0022b5cd74531406e96377d62f2bf5f2ad50ee33744e8d069bebcc8a822cb0f033dda637affeae4a3de26e83c4fdb81a3ac508f669c1c21cb701f1abb872b8f2d86f5019dd6518773765170cfc197eae53642bffc82277be85e589b5a58dae8ff858966aef15d6208c5265b59cfc9137bd9651bb07d237c072ef922e26de64971b98e,youtube-new:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F4549%2F466349%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D43423d2714d01897f273e2d2ac0bb21221e1bfb682cc4e40cbec7e78d4637adc8f440073e2d5e3667b056cf82d66f094223ea0943c2d3dabd893c8233815f21ca47131f72f8cbe7613d80a00ff323b76c6b01d5a72f89e4d68aaa35adc3c12e3d461934fe8fb1a040c87cf5d21bf924aeead5ff34a7aa9b401a0c9951fa685de16b7bcec7e1948299f712ed49d64d8d422ac8a20850adcbe24db6f0d58a6f9ec337897913dc152e2f4ced37188046ab0ff7616a3e89368103d8710c0d32da063cfca4d7d224d4149c5035139dbd84ff1df5567e2faed5e5a8c21fadba2bd80b362f8a7ee09facdacafa261a52dfbd6f3cd0db4c44d5d3cbc91a87e3c1a7bafd6,188-million-us-wildfires:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F2478%2F1151655%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D9a3cf162893afe132651b915b7ad32fb47124afc8fc785f860e2589400aec856e9d79dacf518c2cb882edee41f70edfbabbefc6eeec87c9df4ec5bc1298a545de00190fdea2baf9732749241f2eeac1318f400274d1c51069463ec89e229300c65a2c7c00546f78cb3af13f20fc04c37151b7d16238bc7323a908d40d52d269a0f3f2fb4bddb21ddaee22fd68eaf3fc4dd91c1aa797fb2982ee1507f9e60f2379f83feb02635beed442e66b32a949d33f4199cf4cb3718022b0429f64f37a5b234119cabd55ffb6fb21f32d55498133ce88c47a5dc0b8e4cc71d3fa9ec4bc2ee85c3e971d2f1e75e6d12c0823ca8f4565a33676cf925c5885b69026a50aaae55,publicassistance:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F10128%2F5438389%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240526%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240526T174122Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D9cc468276758f67587473207d9db4c91d955fb36450b769c15c965cb59d203862d5709b9fdc35045347ca6d5d634afca272b9550e725c1b0af4432fb2275f5de0579d1278c0fe34c59c6c3d4f810a2b2918d0394233fa7f47ffd27aeecaf094b2b7ba6a10ed015728314f4e66dc0528c1021cdbeac8a2de2fcf2d7b4b0a2d005bef95aaab081534f63a23db78c902bddc45271020bb76d0cfb815fc09f07e749cf29f2081a6c388649990b6fd2e4d9a71ed1cd0b9335a2bf6503cb1048cf06f73d58de2aeaaea36c9a1fc51ae81c429979762da03a5726482c7e46dcd75923dd47e52ac2cba9af9708bd02bf85b8323e68d95b99e1c537683662f9fd1ae62527'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

"""**This notebook is an exercise in the [Pandas](https://www.kaggle.com/learn/pandas) course.  You can reference the tutorial at [this link](https://www.kaggle.com/residentmario/creating-reading-and-writing).**

---

# Introduction

The first step in most data analytics projects is reading the data file. In this exercise, you'll create Series and DataFrame objects, both by hand and by reading data files.

Run the code cell below to load libraries you will need (including code to check your answers).
"""

import pandas as pd
pd.set_option('display.max_rows', 5)
from learntools.core import binder; binder.bind(globals())
from learntools.pandas.creating_reading_and_writing import *
print("Setup complete.")

"""# Exercises

## 1.

In the cell below, create a DataFrame `fruits` that looks like this:

![](https://storage.googleapis.com/kaggle-media/learn/images/Ax3pp2A.png)
"""

# Your code goes here. Create a dataframe matching the above diagram and assign it to the variable fruits.
fruits = pd.DataFrame({"Apples" : [30], "Bananas": [21]})

# Check your answer
q1.check()
fruits

#q1.hint()
#q1.solution()api

"""## 2.

Create a dataframe `fruit_sales` that matches the diagram below:

![](https://storage.googleapis.com/kaggle-media/learn/images/CHPn7ZF.png)
"""

# Your code goes here. Create a dataframe matching the above diagram and assign it to the variable fruit_sales.
fruit_sales = pd.DataFrame({'Apples': [35, 41],
              'Bananas': [21, 34]},
             index=['2017 Sales', '2018 Sales'])

# Check your answer
q2.check()
fruit_sales

#q2.hint()
#q2.solution()

"""## 3.

Create a variable `ingredients` with a Series that looks like:

```
Flour     4 cups
Milk       1 cup
Eggs     2 large
Spam       1 can
Name: Dinner, dtype: object
```
"""

ingredients = pd.Series(["4 cups", "1 cup", "2 large", "1 can"],
                       index = ["Flour", "Milk", "Eggs", "Spam"],
                       name = "Dinner")

# Check your answer
q3.check()
ingredients

#q3.hint()
#q3.solution()

"""## 4.

Read the following csv dataset of wine reviews into a DataFrame called `reviews`:

![](https://storage.googleapis.com/kaggle-media/learn/images/74RCZtU.png)

The filepath to the csv file is `../input/wine-reviews/winemag-data_first150k.csv`. The first few lines look like:

```
,country,description,designation,points,price,province,region_1,region_2,variety,winery
0,US,"This tremendous 100% varietal wine[...]",Martha's Vineyard,96,235.0,California,Napa Valley,Napa,Cabernet Sauvignon,Heitz
1,Spain,"Ripe aromas of fig, blackberry and[...]",Carodorum Selección Especial Reserva,96,110.0,Northern Spain,Toro,,Tinta de Toro,Bodega Carmen Rodríguez
```
"""

reviews = pd.read_csv("../input/wine-reviews/winemag-data_first150k.csv", index_col=0)

# Check your answer
q4.check()
reviews

#q4.hint()
#q4.solution()

"""## 5.

Run the cell below to create and display a DataFrame called `animals`:
"""

animals = pd.DataFrame({'Cows': [12, 20], 'Goats': [22, 19]}, index=['Year 1', 'Year 2'])
animals

"""In the cell below, write code to save this DataFrame to disk as a csv file with the name `cows_and_goats.csv`."""

# Your code goes here
animals.to_csv("cows_and_goats.csv")
# Check your answer
q5.check()

#q5.hint()
#q5.solution()

"""# Keep going

Move on to learn about **[indexing, selecting and assigning](https://www.kaggle.com/residentmario/indexing-selecting-assigning)**.

---




*Have questions or comments? Visit the [course discussion forum](https://www.kaggle.com/learn/pandas/discussion) to chat with other learners.*
"""