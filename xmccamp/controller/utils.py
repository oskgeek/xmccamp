import pyexcel
import pyexcel.ext.xlsx

from controller.models import Cadet, Parent, Session


def register_cadets(file_path, msg=None):
    msg = dict(Status='UNKNOWN', Error=[]) if not msg else msg
    excel_field_mappings = {'Participant':
        ['Participant: Name', 'Participant: Age as of today', 'Participant: Gender',
         'Participant: Address', 'Participant: Home phone number',
         'Participant: Age as of session', 'Participant: City', 'Participant: Country',
         'Participant: Date of birth', 'Participant: Email address',
         'Participant: State', 'Participant: USAC Training Program', 'Participant: Zip code',
         'Participant: Please explain what you would like to have your son or daugher accomplish while at camp?  Explain any special situations or other information the staff should know about your child.'],
     'Primary P/G' :
         ['Primary P/G: Name', 'Primary P/G: Business phone number',
         'Primary P/G: Cell phone number', 'Primary P/G: Email address',
         'Primary P/G: First name', 'Primary P/G: Gender', 'Primary P/G: Home phone number',
         'Primary P/G: Last name'],
     'Secondary P/G':
         ['Secondary P/G: Business phone number', 'Secondary P/G: Cell phone number',
         'Secondary P/G: Email address', 'Secondary P/G: First name', 'Secondary P/G: Gender',
         'Secondary P/G: Home phone number', 'Secondary P/G: Last name', 'Secondary P/G: Name'],
     'Session' :
         ['Session name', 'Session end date', 'Session location', 'Session start date', 'Session type']
    }
    try:
        sheet = pyexcel.get_sheet(filepath)
        sheet_values = sheet.to_array()
        if len(sheet_values) > 0:
            excel_field_mappings_copy = dict(excel_field_mappings)
            named_column = sheet_values[0]
            for key, desired_col_names in dict(excel_field_mappings).items():
                excel_field_mappings_copy[key] = {}
                for idx, col_name in enumerate(named_column):
                    if col_name in desired_col_names:
                        excel_field_mappings_copy[key].update({idx: col_name})
            row_values = sheet_values[1:]

            for row in row_values:



    except Exception as ex:
        msg['Status'] = 'FAILED'
        msg['Error'].append(repr(ex))
