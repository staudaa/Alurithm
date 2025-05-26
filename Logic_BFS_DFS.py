graf_labirin = {
    'IN': {
        'benar': 'B1',
        'salah': 'S1'
    },
    'B1': {
        'benar': 'OUT',
        'salah': 'IN'
    },
    'S1': {
        'benar': 'OUT',
        'salah': 'IN'
    },
    'OUT': {}
}

def rute_gabungan(graf_labirin, simpul_mulai, jawaban_user):
    rute_dilalui = []
    antrian = [(simpul_mulai, 0)]  

    while antrian:
        simpul, indeks = antrian.pop(0) 
        rute_dilalui.append(simpul)

        if simpul == 'OUT' or indeks >= len(jawaban_user):
            break  

        hasil = jawaban_user[indeks] 
        if hasil in graf_labirin[simpul]:
            next_simpul = graf_labirin[simpul][hasil]
            antrian.append((next_simpul, indeks + 1))

    return rute_dilalui

hasil_user = ['salah', 'salah', 'benar', 'benar']  #contoh simulasi aja (nnti klo udh diimplementasikan ke soal bisa diganti sesuai input user dengan baca csvnya)
print("Rute Labirin yang dilalui:", " → ".join(rute_gabungan(graf_labirin, 'IN', hasil_user)))