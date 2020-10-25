import csv
import requests

with open('Data1000Movies.csv', 'r') as f:
    with open('Data1000MoviesWithImage', 'w') as ff:
        writer = csv.writer(ff, lineterminator='\n')
        reader = csv.reader(f)
        all = []
        row = next(reader)
        row.append('Poster')
        all.append(row)

        url = 'http://www.omdbapi.com/?i=tt3896198&apikey=f587b865'
        for row in reader:
            payload = {"t": row[1], "y": row[6]}
            r = requests.get(url=url, params=payload)
            data = r.json()
            image_url = ""
            try:
                image_url = data["Poster"]
            except KeyError:
                pass

            row.append(image_url)
            all.append(row)

        writer.writerows(all)
