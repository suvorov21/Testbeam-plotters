h = []
var = []
var_data = []

title = []
title_gen = ''
func = ''

bins = []
bin_s = []
bin_e = []

bins_data = []
bin_s_data = []
bin_e_data = []

gr_mc = ROOT.TGraphErrors()
gr_data = ROOT.TGraphErrors()

# common cuts
name = ['0 mm', '1 mm', '2 mm', '3 mm', '4 mm', '5 mm']
color = [ROOT.kRed, ROOT.kViolet, ROOT.kBlue, ROOT.kBlack, ROOT.kGreen, ROOT.kMagenta]
tol = 0.0005
cut = [f'multiplicity > 1 && abs(dx[][0] - 0.000) < {tol}',
       f'multiplicity > 1 && abs(dx[][0] - 0.001) < {tol}',
       f'multiplicity > 1 && abs(dx[][0] - 0.002) < {tol}',
       f'multiplicity > 1 && abs(dx[][0] - 0.003) < {tol}',
       f'multiplicity > 1 && abs(dx[][0] - 0.004) < {tol}',
       f'multiplicity > 1 && abs(dx[][0] - 0.005) < {tol}'
      ]
ls = [0, 1, 2, 3, 4, 5]
opt = ['l', 's', 't']

def set_charge():
    global var, var_data, title, title_gen, func, bins, bin_s, bin_e, bins_data, bin_s_data, bin_e_data
    var = ['pad_charge[][0]', 'pad_charge[][1]', 'pad_charge[][2]']
    var_data = var

    title = ['Q_{1}', 'Q_{2}', 'Q_{3}']
    title_gen = 'Q_{i}'
    func = 'landau'

    bins = [200, 200, 200]
    bin_s = [0., 0, 0]
    bin_e = [4000, 1500, 400]
    
    bins_data = bins
    bin_s_data = bin_s
    bin_e_data = bin_e
    
def set_charge_r():
    global var, var_data, title, title_gen, func, bins, bin_s, bin_e, bins_data, bin_s_data, bin_e_data
    var = ['pad_charge[][0]', 'pad_charge[][1] / pad_charge[][0]', 'pad_charge[][2] / pad_charge[][0]']
    var_data = var

    title = ['Q_{1}', 'Q_{2}/Q_{1}', 'Q_{3}/Q_{1}']
    title_gen = 'Q_{i} / Q_{1}'
    func = 'landau'

    bins = [200, 210, 200]
    bin_s = [0., 0, 0]
    bin_e = [4000, 1.1, 0.3]

    bins_data = bins
    bin_s_data = bin_s
    bin_e_data = bin_e
    
def set_time():
    global var, var_data, title, title_gen, func, bins, bin_s, bin_e, bins_data, bin_s_data, bin_e_data
    var = ['pad_charge[][0]', 'pad_time[][1] - pad_time[][0]', 'pad_time[][2] - pad_time[][0]']
    var_data = ['pad_charge[][0]', '(pad_time[][1] - pad_time[][0])*5/4', '(pad_time[][2] - pad_time[][0])*5/4']
    title = ['Q_{1}', 't_{2} - t_{1}', 't_{3} - t_{1}']
    title_gen = 't_{i} - t_{1}'
    func = 'gaus'

    bins = [200, 30, 80]
    bin_s = [0., 0, 0]
    bin_e = [4000, 30, 80]

    bins_data = [200, 24, 64]
    bin_s_data = bin_s
    bin_e_data = bin_e
    
def set_fwhm():
    global var, var_data, title, title_gen, func, bins, bin_s, bin_e, bins_data, bin_s_data, bin_e_data
    var = ['wf_fwhm[][0]', 'wf_fwhm[][1]', 'wf_fwhm[][2]']
    var_data = ['wf_fwhm[][0] * 5/4', 'wf_fwhm[][1] * 5/4', 'wf_fwhm[][2] * 5/4']
    title = ['FWHM WF leading', 'FWHM WF second', 'FWHM WF third']
    title_gen = 'WF FWHM'
    func = 'landau'

    bins = [30, 50, 100]
    bin_s = [0., 0, 0]
    bin_e = [30, 50, 100]

    bins_data = [24, 40, 80]
    bin_s_data = [0., 0, 0]
    bin_e_data = [30, 50, 100]

def draw():
    global h
    h = []
    hs = []
    ev_prev = -1
    hs.append(ROOT.THStack('hsl', ''))
    hs.append(ROOT.THStack('hss', ''))
    hs.append(ROOT.THStack('hst', ''))

    # working on MC
    for o_num, o in enumerate(opt):
        for i in ls:
            print(f'MC {o} {i}\r', end='')
            h.append(ROOT.TH1F(f'h_mc_{o}_{name[i]}', '', bins[o_num], bin_s[o_num], bin_e[o_num]))
            file_mc[0].outtree.Project(f'h_mc_{o}_{name[i]}', var[o_num], cut[i])
            h[-1].SetLineStyle(2)
            h[-1].SetLineColor(color[i])
            h[-1].Scale(1./h[-1].Integral())
            hs[o_num].Add(h[-1])

    # working on DATA
    for o_num, o in enumerate(opt):
        for i in ls:
            print(f'DATA {o} {i}\r', end='')
            h.append(ROOT.TH1F(f'h_data_{o}_{name[i]}', '', bins_data[o_num], bin_s_data[o_num], bin_e_data[o_num]))
            file_data[0].outtree.Project(f'h_data_{o}_{name[i]}', var_data[o_num], cut[i])
            h[-1].SetLineColor(color[i])
            h[-1].Scale(1./h[-1].Integral())
            hs[o_num].Add(h[-1])
            
def draw_gr():
    global gr_mc, gr_data, h, func
    def getVal(h):
    #     return h.GetMean()
        h.Fit(func, 'Q')
        h.Fit(func, 'Q')
        return h.GetFunction(func).GetParameter(1)

    def getValErr(h):
    #     return h.GetMeanError()
        h.Fit(func, 'Q')
        return h.GetFunction(func).GetParError(1)

    def set_gr(gr, col, marker):
        gr.SetMarkerStyle(marker)
        gr.SetLineColor(col)
        gr.SetMarkerColor(col)

    def GetX(num_mc, opt):
        if opt == 'l':
            return ls[num_mc[opt]]
        elif opt == 's':
            return -ls[num_mc[opt]] + 10.19
        elif opt == 't':
            return ls[num_mc[opt]] + 10.19


    gr_data = ROOT.TGraphErrors()
    set_gr(gr_data, ROOT.kBlack, 22)
    num_mc = {'l': 0, 's': 0, 't': 0}
    #  process DATA
    for i in range(len(h)):
        # leading pad
        parse = h[i].GetName().split('_')
        if num_mc[parse[2]] < len(name) and parse[1] == 'data' and parse[3] == name[num_mc[parse[2]]] and parse[2] in opt:
            gr_data.SetPoint(gr_data.GetN(), GetX(num_mc, parse[2]), getVal(h[i]))
            gr_data.SetPointError(gr_data.GetN()-1, 0, getValErr(h[i]))
            num_mc[parse[2]] += 1

    # process MC
    gr_mc = ROOT.TGraphErrors()
    set_gr(gr_mc, ROOT.kRed, 22)

    gr_ratio = ROOT.TGraphErrors()
    set_gr(gr_ratio, ROOT.kRed, 22)

    num_mc = {'l': 0, 's': 0, 't': 0}
    mult = {'l': 0, 's': 1, 't': 2}
    for i in range(len(h)):
        parse = h[i].GetName().split('_')
        if num_mc[parse[2]] < len(name) and parse[1] == 'mc' and parse[3] == name[num_mc[parse[2]]] and parse[2] in opt: 
            gr_mc.SetPoint(gr_mc.GetN(), GetX(num_mc, parse[2]), getVal(h[i]))
            gr_mc.SetPointError(gr_mc.GetN()-1, 0, getValErr(h[i]))

            data_point = ls.index(num_mc[parse[2]]) + mult[parse[2]]*len(ls)
            ratio = getVal(h[i]) / gr_data.GetY()[data_point]
            un_a = getValErr(h[i]) / getVal(h[i])
            un_b = gr_data.GetErrorY(data_point) / gr_data.GetY()[data_point]
            gr_ratio.SetPoint(gr_ratio.GetN(), GetX(num_mc, parse[2]), ratio)
            gr_ratio.SetPointError(gr_ratio.GetN()-1, 0, ratio*((un_a*un_a + un_b*un_b)**0.5))
            num_mc[parse[2]] += 1
            

path = '/eos/user/s/ssuvorov/DESY_testbeam/high_stat_respin_v2/'
file_mc = [ROOT.TFile(path + '/s_412_430_02T_iter9.root', 'READ')]

path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/z_scan2/'
file_data = [ROOT.TFile(path + '/z_412ns_275V_m40_iter4.root', 'READ')]

set_charge_r()
draw()
draw_gr()
charge_r_data19 = gr_mc.Clone()
charge_r_data21 = gr_data.Clone()

set_charge()
draw()
draw_gr()
charge_data19 = gr_mc.Clone()
charge_data21 = gr_data.Clone()

set_time()
draw()
draw_gr()
time_data19 = gr_mc.Clone()
time_data21 = gr_data.Clone()

set_fwhm()
draw()
draw_gr()
fwhm_data19 = gr_mc.Clone()
fwhm_data21 = gr_data.Clone()


path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
file_mc = [ROOT.TFile(path + '/z_400_nomDrift_5cm_iter4.root')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/z_respin/'
# file_data = [ROOT.TFile(path + '/z_412ns_275V_m40_iter4.root', 'READ')]

set_charge_r()
draw()
draw_gr()
charge_r_mc_new = gr_mc.Clone()
# charge_r_data21 = gr_data.Clone()

set_charge()
draw()
draw_gr()
charge_mc_new = gr_mc.Clone()
# charge_data21 = gr_data.Clone()

set_time()
draw()
draw_gr()
time_mc_new = gr_mc.Clone()
# time_data21 = gr_data.Clone()

set_fwhm()
draw()
draw_gr()
fwhm_mc_new = gr_mc.Clone()
# fwhm_data21 = gr_data.Clone()

path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
file_mc = [ROOT.TFile(path + '/z_400_nomDrift_5cm_RC100_iter4.root')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/z_respin/'
# file_data = [ROOT.TFile(path + '/z_412ns_275V_m40_iter4.root', 'READ')]

set_charge_r()
draw()
draw_gr()
charge_r_mc_RC100 = gr_mc.Clone()
# charge_r_data21 = gr_data.Clone()

set_charge()
draw()
draw_gr()
charge_mc_RC100 = gr_mc.Clone()
# charge_data21 = gr_data.Clone()

set_time()
draw()
draw_gr()
time_mc_RC100 = gr_mc.Clone()
# time_data21 = gr_data.Clone()

set_fwhm()
draw()
draw_gr()
fwhm_mc_RC100 = gr_mc.Clone()
# fwhm_data21 = gr_data.Clone()







# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v24/z95_v24_iter4.root')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/z_respin/'
# file_data = [ROOT.TFile(path + '/z_412ns_275V_m40_iter4.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc24 = gr_mc.Clone()
# charge_r_data21 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc24 = gr_mc.Clone()
# charge_data21 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc24 = gr_mc.Clone()
# time_data21 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc24 = gr_mc.Clone()
# fwhm_data21 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v28/z95_v28_iter4.root')]

# # path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# # file_data = [ROOT.TFile(path + '/v25/z95_v25_iter4.root')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc28 = gr_mc.Clone()
# charge_r_data21 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc28 = gr_mc.Clone()
# charge_data21 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc28 = gr_mc.Clone()
# time_data21 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc28 = gr_mc.Clone()
# fwhm_data21 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z95_v26_iter4.root')]

# # path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# # file_data = [ROOT.TFile(path + '/v25/z95_v25_iter4.root')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc26 = gr_mc.Clone()
# charge_r_data21 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc26 = gr_mc.Clone()
# charge_data21 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc26 = gr_mc.Clone()
# time_data21 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc26 = gr_mc.Clone()
# fwhm_data21 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v29/z95_v29_iter4.root')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/z_respin/'
# file_data = [ROOT.TFile(path + '/z_412ns_275V_m40_iter4.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc29 = gr_mc.Clone()
# # charge_r_data21 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc29 = gr_mc.Clone()
# # charge_data21 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc29 = gr_mc.Clone()
# # time_data21 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc29 = gr_mc.Clone()
# # fwhm_data21 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v30/z95_v30_iter4.root')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/z_respin/'
# file_data = [ROOT.TFile(path + '/z_412ns_275V_m40_iter4.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc30 = gr_mc.Clone()
# # charge_r_data21 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc30 = gr_mc.Clone()
# # charge_data21 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc30 = gr_mc.Clone()
# # time_data21 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc30 = gr_mc.Clone()
# # fwhm_data21 = gr_data.Clone()








# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v24/z90_v24_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_0_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc55 = gr_mc.Clone()
# charge_r_data21_y0 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc55 = gr_mc.Clone()
# charge_data21_y0 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc55 = gr_mc.Clone()
# time_data21_y0 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc55 = gr_mc.Clone()
# fwhm_data21_y0 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z90_v26_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_40_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc100 = gr_mc.Clone()
# charge_r_data21_y40 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc100 = gr_mc.Clone()
# charge_data21_y40 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc100 = gr_mc.Clone()
# time_data21_y40 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc100 = gr_mc.Clone()
# fwhm_data21_y40 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z90_v26_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_80_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc100 = gr_mc.Clone()
# charge_r_data21_y80 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc100 = gr_mc.Clone()
# charge_data21_y80 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc100 = gr_mc.Clone()
# time_data21_y80 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc100 = gr_mc.Clone()
# fwhm_data21_y80 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z90_v26_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_100_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc100 = gr_mc.Clone()
# charge_r_data21_y100 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc100 = gr_mc.Clone()
# charge_data21_y100 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc100 = gr_mc.Clone()
# time_data21_y100 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc100 = gr_mc.Clone()
# fwhm_data21_y100 = gr_data.Clone()


# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z90_v26_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_m40_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc100 = gr_mc.Clone()
# charge_r_data21_ym40 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc100 = gr_mc.Clone()
# charge_data21_ym40 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc100 = gr_mc.Clone()
# time_data21_ym40 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc100 = gr_mc.Clone()
# fwhm_data21_ym40 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z90_v26_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_m80_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc100 = gr_mc.Clone()
# charge_r_data21_ym80 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc100 = gr_mc.Clone()
# charge_data21_ym80 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc100 = gr_mc.Clone()
# time_data21_ym80 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc100 = gr_mc.Clone()
# fwhm_data21_ym80 = gr_data.Clone()

# path = '/eos/experiment/neutplatform/np07/HAT/MC/ana_results/'
# file_mc = [ROOT.TFile(path + '/v26/z90_v26_iter4.root', 'READ')]

# path = '/eos/experiment/neutplatform/np07/HAT/DESY_2021/ana_output/y_scan2/'
# file_data = [ROOT.TFile(path + '/y_m120_iter9.root', 'READ')]

# set_charge_r()
# draw()
# draw_gr()
# charge_r_mc100 = gr_mc.Clone()
# charge_r_data21_ym120 = gr_data.Clone()

# set_charge()
# draw()
# draw_gr()
# charge_mc100 = gr_mc.Clone()
# charge_data21_ym120 = gr_data.Clone()

# set_time()
# draw()
# draw_gr()
# time_mc100 = gr_mc.Clone()
# time_data21_ym120 = gr_data.Clone()

# set_fwhm()
# draw()
# draw_gr()
# fwhm_mc100 = gr_mc.Clone()
# fwhm_data21_ym120 = gr_data.Clone()
