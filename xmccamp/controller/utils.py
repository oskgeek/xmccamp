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
         'Primary P/G: Gender', 'Primary P/G: Home phone number'],
     'Secondary P/G':
         ['Secondary P/G: Business phone number', 'Secondary P/G: Cell phone number',
         'Secondary P/G: Email address', 'Secondary P/G: Gender',
         'Secondary P/G: Home phone number', 'Secondary P/G: Name'],
     'Session' :
         ['Session name', 'Session end date', 'Session location', 'Session start date', 'Session type']
    }
    try:
        sheet = pyexcel.get_sheet(file_path)
        sheet_values = sheet.to_array()
        if len(sheet_values) > 0:
            excel_field_mappings_copy = {}
            named_column = sheet_values[0]
            for key, desired_col_names in dict(excel_field_mappings).items():
                for idx, col_name in enumerate(named_column):
                    if col_name in desired_col_names:
                        excel_field_mappings_copy.update({idx: col_name})
            
            row_values = sheet_values[1:]
            for row in row_values:
                field_dict = {}
                for field_id, field_value in enumerate(row):
                    try:
                        field_dict[excel_field_mappings_copy[field_id]] = field_value
                    except KeyError:
                        pass
                
                if not any(field_dict.values()):
                    continue
                print "creating parents"
                primary_parent_obj = Parent()
                pp_status = primary_parent_obj.create_parent_by_fields(field_dict, 'P')
                
                secondary_parent_obj = Parent()
                sp_status = secondary_parent_obj.create_parent_by_fields(field_dict, 'S')
                
                
                print "creating sessions"
                session_obj = Session()
                session_obj.parse_fields(field_dict)
                session_obj.save()
                
                print "creating cadet profile"
                cadet_obj = Cadet()
                cd_status = cadet_obj.parse_fields(field_dict)
                if cd_status:
                    if pp_status:
                        cadet_obj.primary_parent = primary_parent_obj
                        
                        if sp_status:
                            cadet_obj.secondary_parent = secondary_parent_obj
                        else:
                            cadet_obj.secondary_parent = primary_parent_obj
                            
                        cadet_obj.sessions = session_obj
                        cadet_obj.save()


    except Exception as ex:
        msg['Status'] = 'FAILED'
        msg['Error'].append(repr(ex))
