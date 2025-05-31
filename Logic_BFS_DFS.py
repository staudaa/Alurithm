graf_labirin = {
    'IN': {
        'benar': 'B1',
        'salah': 'S1'
    },
    'B1': {
        'benar': 'OUT',
        'salah': 'S1'
    },
    'S1': {
        'benar': 'S2',
        'salah': 'L1'
    },
    'S2': {
        'benar': 'OUT',
        'salah': 'L1'
    },
    'L1': {
        'benar': 'L2',
        'salah': 'L1'
    },
    'L2': {
        'benar': 'L3',
        'salah': 'L1'
    },
    'L3': {
        'benar': 'OUT',
        'salah': 'L2'
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

# hasil_user = ['salah', 'salah', 'benar', 'benar']  #contoh simulasi aja (nnti klo udh diimplementasikan ke soal bisa diganti sesuai input user dengan baca csvnya)
# print("Rute Labirin yang dilalui:", " → ".join(rute_gabungan(graf_labirin, 'IN', hasil_user)))