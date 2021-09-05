import ROOT

file = ROOT.TFile('/eos/user/s/ssuvorov/DESY_testbeam/test_iter0.root')
Nevents = 1e6

with open('tmp/test.txt', 'w') as f:
    f.write('event\tcolumn\tfit_pos\tcluster_pos\tpad_charge\tpad_row\tpad_time\n')
    for num, entry in enumerate(file.outtree):
        if num > Nevents: break

        print(f'\rEvent {num}', end='')

        for col in range(36):
            # column is empty
            if entry.pad_x[col*10] == -999: continue
            charge = str(entry.pad_charge[col*10])
            pad_y = str(entry.pad_y[col*10])
            time = str(entry.pad_time[col*10])
            # merge charge/time/pos info
            for row in range(1, 10):
                if entry.pad_charge[col*10+row] < 0: break
                charge += f':{entry.pad_charge[col*10+row]}'
                pad_y += f':{entry.pad_y[col*10+row]}'
                time += f':{entry.pad_time[col*10+row]}'

            f.write('\t'.join([
                              str(entry.ev),
                              str(entry.pad_x[col*10]),
                              str(entry.track_pos[col]),
                              str(entry.clust_pos[col]),
                              charge,
                              pad_y,
                              time
                              ]) + '\n')

            for row in range(0, 10):
                maxim = -250
                for time in range(520):
                    adc = entry.pad_wf_q[col*10*520 + 520*row + time]
                    if adc > maxim:
                        maxim = adc

                if maxim < -249: continue

                f.write('time_bin\tadc\n')
                for time in range(520):
                    adc = entry.pad_wf_q[col*10*520 + 520*row + time]
                    if adc != -999 and adc != -250:
                        f.write('\t'.join([str(time),
                                          str(adc)
                                          ]) + '\n')

    print('')

