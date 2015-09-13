def name_clean(m):
    """ Returns corresponding intelligble name """
    known = {'Beamwidth_Fixed': 'Noise-only',
             'Beamwidth_Perera': 'Switching',
             'Beamwidth_Jones': 'Modified-Gaussian Precession',
             'Beamwidth_Jones_FixedP': 'Modified-Gaussian Precession (fixed P)',
             'Beamwidth_Gaussian': 'Gaussian Precession',
             'Spindown_Perera': 'Switching',
             'Spindown_Precession': 'Precession',
             'Spindown_Precession_FixedP': 'Precession (fixed P)',
             }
    try:
        return known[m]
    except KeyError:
        return m.replace("_", " ")


def get_evidence():
    d = {}
    with open("Evidence.dat", "r") as f:
        for line in f:
            mn, ev, er = line.split(",")
            d[mn] = "{:1.2f}+/-{:1.2f}".format(float(ev), float(er))
    return d



def GenerateTable(title, subtitle, models, comments):

    evidences = []
    for m in models:
        try:
            evidences.append(evidence_dict[m.replace("_", "")])
        except KeyError:
            evidences.append(0)

    rows = ["""  <tr>
    <td><b> Model </b></td>
    <td><b> Plots </b></td>
    <td><b> Evidence </b></td>
    <td><b> Comment </b></td>
  </tr>"""]

    row_template = """
  <tr>
    <td> {pretty_model_name} </td>
    <td>
    <a href="{model_name}_nburn0.png"> Initial </a>
    <a href="{model_name}_nprod.png"> Production </a>
    <a href="{model_name}_PosteriorWithFit.pdf"> Posterior </a>
    </td>
    <td> {evidence}  </td>
    <td> {comment} </td>
  </tr>
  """

    for m, e, c in zip(models, evidences, comments):
        rows.append(row_template.format(model_name=m,
                                        pretty_model_name=name_clean(m),
                                        evidence=e,
                                        comment=c,
                                        ))

    inner = "\n".join(rows)
    outer = """
##{}
<b> Description: </b> {}

<table style="width:100%" border="1|0" cellpadding="4" cellspacing="0" >
{}
</table>

<div style="height:50px;"></div>
"""
    return outer.format(title, subtitle, inner)

header = """---
layout: default
title: B1828-11 Data Analysis Results
---

# B1828-11 Data Analyis Results

"""

evidence_dict = get_evidence()
file_name = "index.md"
with open(file_name, "w+") as f:
    f.write(header)

    title = "Spin-down data"
    subtitle = "uniform prior based on crude estimate to the data"
    models = ["Spindown_Perera", "Spindown_Precession",
              "Spindown_Precession_FixedP"]
    comments = ["", "", "Fixed value of P from ATNF"]
    f.write(GenerateTable(title, subtitle, models, comments))

    title = "Beam-width data"
    subtitle = "uniform prior based on crude estimate to the data"
    models = ["Beamwidth_Perera_Flat", "Beamwidth_Jones_Flat"]
    comments = ["", "", ""]
    f.write(GenerateTable(title, subtitle, models, comments))

    title = "Beam-width data"
    subtitle = "prior from the spin-down data"
    models = ["Beamwidth_Fixed", "Beamwidth_Perera", "Beamwidth_Gaussian",
              "Beamwidth_Jones", "Beamwidth_Jones_FixedP"]
    comments = ["", "", "", "", "Fixed value of P from ATNF"]
    f.write(GenerateTable(title, subtitle, models, comments))

    title = "Averaged beam-width data"
    subtitle = "prior from the spin-down data"
    models = ["BeamwidthAveraged_Perera", "BeamwidthAveraged_Jones"]
    comments = ["", "", "Had to use a flat prior on psi0"]
    f.write(GenerateTable(title, subtitle, models, comments))

    title = "Averaged beam-width data"
    subtitle = "uniform prior based on crude estimate to the data"
    models = ["BeamwidthAveraged_Perera_Flat"]
    comments = [""]
    f.write(GenerateTable(title, subtitle, models, comments))

    f.write("&nbsp;")
