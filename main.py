from pyknow import *
from flask import Flask, request, render_template

diseases_list = []
diseases_scenarios = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

app = Flask(__name__)


@app.route('/')
def home():
    preprocess()
    return render_template('index.html')


@app.route('/disease_diagnosis', methods=['POST'])
def disease_diagnosis():
    if request.method == 'POST':
        if request.form.get('submit') == 'submit':
            symptoms = get_symptoms_from_app(request)
            engine = Diagnosis(symptoms)
            engine.reset()  # Prepare the engine for the execution.
            engine.run()  # Run it!
            """ Rendering results on HTML GUI
            """
            output_id_disease = "The most probable disease that you have is {}".format(engine.get_id_disease())
            output_disease_details = "A short description of the disease is given: {}".format(engine.get_disease_details())
            output_disease_treatments = "The common medications and procedures suggested by other real doctors are: {}".format(engine.get_treatments())
            return render_template('index.html', output_disease=output_id_disease,
                                   output_details=output_disease_details,
                                   output_treatments=output_disease_treatments)
        elif request.form.get('restart') == 'restart':
            return render_template('index.html')


def preprocess():
    global diseases_list, diseases_scenarios, diseases_symptoms, symptom_map, d_desc_map, d_treatment_map
    diseases = open("diseases.txt")
    diseases_t = diseases.read()
    diseases_list = diseases_t.split("\n")
    diseases.close()

    print(diseases_list)

    scenarios = open("scenarios.txt")
    scenarios_t = scenarios.read()
    diseases_scenarios = scenarios_t.split("\n")
    scenarios.close()

    print(diseases_scenarios)

    for scenario in diseases_scenarios:
        disease_s_file = open("Disease Symptoms/" + scenario + ".txt")
        disease_s_data = disease_s_file.read()
        s_list = disease_s_data.split("\n")
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = scenario
        disease_s_file.close()

    for disease in diseases_list:
        disease_s_file = open("Disease Descriptions/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        d_desc_map[disease] = disease_s_data
        disease_s_file.close()

        disease_s_file = open("Disease Treatment/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        d_treatment_map[disease] = disease_s_data
        disease_s_file.close()


def get_symptoms_from_app(request):
    symptoms_list = []
    fever_symptom = 'no'
    cough_symptom = 'no'
    fatigue_symptom = 'no'
    loss_taste_smell_symptom = 'no'
    sore_throat_symptom = 'no'
    headache_symptom = 'no'
    aches_pains_symptom = 'no'
    diarrhea_symptom = 'no'
    chills_symptom = 'no'
    sneeze_symptom = 'no'
    rash_symptom = 'no'
    red_eyes_symptom = 'no'
    difficulty_breathing_symptom = 'no'
    loss_speech_symptom = 'no'
    chest_pain_symptom = 'no'

    if request.method == 'POST':
        if request.form.get('match_fever'):
            fever_symptom = request.form.get('match_fever')

        if request.form.get('match_cough'):
            cough_symptom = request.form.get('match_cough')

        if request.form.get('match_fatigue'):
            fatigue_symptom = request.form.get('match_fatigue')

        if request.form.get('match_loss_taste_smell'):
            loss_taste_smell_symptom = request.form.get('match_loss_taste_smell')

        if request.form.get('match_sore_throat'):
            sore_throat_symptom = request.form.get('match_sore_throat')

        if request.form.get('match_headache'):
            headache_symptom = request.form.get('match_headache')

        if request.form.get('match_aches_pains'):
            aches_pains_symptom = request.form.get('match_aches_pains')

        if request.form.get('match_diarrhea'):
            diarrhea_symptom = request.form.get('match_diarrhea')

        if request.form.get('match_chills'):
            chills_symptom = request.form.get('match_chills')

        if request.form.get('match_sneeze'):
            sneeze_symptom = request.form.get('match_sneeze')

        if request.form.get('match_rash'):
            rash_symptom = request.form.get('match_rash')

        if request.form.get('match_red_eyes'):
            red_eyes_symptom = request.form.get('match_red_eyes')

        if request.form.get('match_difficulty_breathing'):
            difficulty_breathing_symptom = request.form.get('match_difficulty_breathing')

        if request.form.get('match_loss_speech'):
            loss_speech_symptom = request.form.get('match_loss_speech')

        if request.form.get('match_chest_pain'):
            chest_pain_symptom = request.form.get('match_chest_pain')

        print(fever_symptom)
        print(cough_symptom)
        print(fatigue_symptom)
        print(loss_taste_smell_symptom)
        print(sore_throat_symptom)
        print(headache_symptom)
        print(aches_pains_symptom)
        print(diarrhea_symptom)
        print(chills_symptom)
        print(sneeze_symptom)
        print(rash_symptom)
        print(red_eyes_symptom)
        print(difficulty_breathing_symptom)
        print(loss_speech_symptom)
        print(chest_pain_symptom)

        symptoms_list.append(fever_symptom)
        symptoms_list.append(cough_symptom)
        symptoms_list.append(fatigue_symptom)
        symptoms_list.append(loss_taste_smell_symptom)
        symptoms_list.append(sore_throat_symptom)
        symptoms_list.append(headache_symptom)
        symptoms_list.append(aches_pains_symptom)
        symptoms_list.append(diarrhea_symptom)
        symptoms_list.append(chills_symptom)
        symptoms_list.append(sneeze_symptom)
        symptoms_list.append(rash_symptom)
        symptoms_list.append(red_eyes_symptom)
        symptoms_list.append(difficulty_breathing_symptom)
        symptoms_list.append(loss_speech_symptom)
        symptoms_list.append(chest_pain_symptom)

        return symptoms_list


def identify_disease(*arguments):
    symptom_list = []
    for symptom in arguments:
        symptom_list.append(symptom)
    # Handle key error
    return symptom_map[str(symptom_list)]


def get_details(disease):
    return d_desc_map[disease]


def get_treatments_details(disease):
    return d_treatment_map[disease]


class Diagnosis(KnowledgeEngine):

    def __init__(self, symptoms=[], id_disease="", disease_details="", treatments=""):
        self.symptoms = symptoms
        self.id_disease = id_disease
        self.disease_details = disease_details
        self.treatments = treatments
        KnowledgeEngine.__init__(self)

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="find_diagnosis")

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(headache=W())))
    def symptom_0(self):
        self.declare(Fact(headache=self.symptoms[5]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(sore_throat=W())))
    def symptom_1(self):
        self.declare(Fact(sore_throat=self.symptoms[4]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(fever=W())))
    def symptom_2(self):
        self.declare(Fact(fever=self.symptoms[0]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(chest_pain=W())))
    def symptom_3(self):
        self.declare(Fact(chest_pain=self.symptoms[14]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(cough=W())))
    def symptom_4(self):
        self.declare(Fact(cough=self.symptoms[1]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(fatigue=W())))
    def symptom_5(self):
        self.declare(Fact(fatigue=self.symptoms[2]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(loss_taste_smell=W())))
    def symptom_6(self):
        self.declare(Fact(loss_taste_smell=self.symptoms[3]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(aches_pains=W())))
    def symptom_7(self):
        self.declare(Fact(aches_pains=self.symptoms[6]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(diarrhea=W())))
    def symptom_8(self):
        self.declare(Fact(diarrhea=self.symptoms[7]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(chills=W())))
    def symptom_9(self):
        self.declare(Fact(chills=self.symptoms[8]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(rash_discoloration_skin=W())))
    def symptom_10(self):
        self.declare(Fact(rash_discoloration_skin=self.symptoms[10]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(irritated_eyes=W())))
    def symptom_11(self):
        self.declare(Fact(irritated_eyes=self.symptoms[11]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(breath_difficulty=W())))
    def symptom_12(self):
        self.declare(Fact(breath_difficulty=self.symptoms[12]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(loss_speech=W())))
    def symptom_13(self):
        self.declare(Fact(loss_speech=self.symptoms[13]))

    @Rule(Fact(action='find_diagnosis'), NOT(Fact(sneezing=W())))
    def symptom_14(self):
        self.declare(Fact(sneezing=self.symptoms[9]))

    # Rule combination for COVID 19 and other diseases diagnosis
    @Rule(Fact(action='find_diagnosis'), Fact(headache="yes"), Fact(sore_throat="yes"), Fact(fever="no"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_0(self):
        self.declare(Fact(disease="COVID-19 Scenario 1"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="no"), Fact(fever="no"),
          Fact(chest_pain="yes"),
          Fact(cough="yes"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_1(self):
        self.declare(Fact(disease="COVID-19 Scenario 2"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="yes"), Fact(sore_throat="no"), Fact(fever="no"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="yes"))
    def disease_2(self):
        self.declare(Fact(disease="Common Cold Scenario 1"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="yes"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="yes"), Fact(fatigue="yes"), Fact(loss_taste_smell="no"), Fact(aches_pains="yes"),
          Fact(diarrhea="no"), Fact(chills="yes"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="yes"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="yes"))
    def disease_3(self):
        self.declare(Fact(disease="Flu"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="yes"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="yes"), Fact(fatigue="yes"), Fact(loss_taste_smell="no"), Fact(aches_pains="yes"),
          Fact(diarrhea="no"), Fact(chills="yes"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="yes"), Fact(breath_difficulty="yes"),
          Fact(loss_speech="no"), Fact(sneezing="yes"))
    def disease_4(self):
        self.declare(Fact(disease="COVID-19 Scenario 3"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="yes"), Fact(fever="no"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_5(self):
        self.declare(Fact(disease="Common Cold Scenario 2"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_6(self):
        self.declare(Fact(disease="Common Cold Scenario 3"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="no"), Fact(fever="no"),
          Fact(chest_pain="yes"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_7(self):
        self.declare(Fact(disease="COVID-19 Scenario 4"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="yes"),
          Fact(loss_speech="yes"), Fact(sneezing="no"))
    def disease_8(self):
        self.declare(Fact(disease="COVID-19 Scenario 5"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="yes"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="yes"), Fact(fatigue="no"), Fact(loss_taste_smell="yes"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_9(self):
        self.declare(Fact(disease="COVID-19 Scenario 6"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="yes"), Fact(irritated_eyes="yes"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="no"))
    def disease_10(self):
        self.declare(Fact(disease="Allergies Scenario 1"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="yes"), Fact(fever="no"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="yes"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="yes"))
    def disease_11(self):
        self.declare(Fact(disease="Common Cold Scenario 4"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="no"), Fact(fever="yes"),
          Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="yes"))
    def disease_12(self):
        self.declare(Fact(disease="Common Cold Scenario 5"))

    @Rule(Fact(action='find_diagnosis'), Fact(headache="no"), Fact(sore_throat="yes"), Fact(fever="no"),
          Fact(chest_pain="no"),
          Fact(cough="yes"), Fact(fatigue="no"), Fact(loss_taste_smell="no"), Fact(aches_pains="no"),
          Fact(diarrhea="no"), Fact(chills="no"),
          Fact(rash_discoloration_skin="no"), Fact(irritated_eyes="no"), Fact(breath_difficulty="no"),
          Fact(loss_speech="no"), Fact(sneezing="yes"))
    def disease_13(self):
        self.declare(Fact(disease="Allergies Scenario 2"))

    @Rule(Fact(action='find_diagnosis'), Fact(disease=MATCH.disease), salience=-998)
    def disease(self, disease):
        print(disease)
        if "COVID-19" in disease:
            self.id_disease = "COVID-19"
            print(self.id_disease)
        elif "Cold" in disease:
            self.id_disease = "Common Cold"
            print(self.id_disease)
        elif "Flu" in disease:
            self.id_disease = "Flu"
            print(self.id_disease)
        else:
            self.id_disease = "Allergies"
            print(self.id_disease)

        self.disease_details = get_details(self.id_disease)
        self.treatments = get_treatments_details(self.id_disease)
        print(self.disease_details)
        print(self.treatments)

    @Rule(Fact(action='find_diagnosis'),
          Fact(headache=MATCH.headache),
          Fact(sore_throat=MATCH.sore_throat),
          Fact(fever=MATCH.fever),
          Fact(chest_pain=MATCH.chest_pain),
          Fact(cough=MATCH.cough),
          Fact(fatigue=MATCH.fatigue),
          Fact(loss_taste_smell=MATCH.loss_taste_smell),
          Fact(aches_pains=MATCH.aches_pains),
          Fact(diarrhea=MATCH.diarrhea),
          Fact(chills=MATCH.chills),
          Fact(rash_discoloration_skin=MATCH.rash_discoloration_skin),
          Fact(irritated_eyes=MATCH.irritated_eyes),
          Fact(breath_difficulty=MATCH.breath_difficulty),
          Fact(loss_speech=MATCH.loss_speech),
          Fact(sneezing=MATCH.sneezing), NOT(Fact(disease=MATCH.disease)), salience=-999)
    def not_matched(self, headache, sore_throat, fever, chest_pain, cough, fatigue, loss_taste_smell, aches_pains,
                    diarrhea, chills, rash_discoloration_skin, irritated_eyes, breath_difficulty, loss_speech,
                    sneezing):
        print("\nDid not find any disease that matches your exact symptoms")
        lis = [headache, sore_throat, fever, chest_pain, cough, fatigue, loss_taste_smell, aches_pains,
               diarrhea, chills, rash_discoloration_skin, irritated_eyes, breath_difficulty, loss_speech, sneezing]
        max_count = 0
        max_disease = ""
        for key, val in symptom_map.items():
            count = 0
            temp_list = eval(key)
            for j in range(0, len(lis)):
                if temp_list[j] == lis[j] and lis[j] == "yes":
                    count = count + 1
            if count > max_count:
                max_count = count
                max_disease = val
        if "COVID-19" in max_disease:
            self.id_disease = "COVID-19"
            print(self.id_disease)
        elif "Cold" in max_disease:
            self.id_disease = "Common Cold"
            print(self.id_disease)
        elif "Flu" in max_disease:
            self.id_disease = "Flu"
            print(self.id_disease)
        else:
            self.id_disease = "Allergies"
            print(self.id_disease)

        self.disease_details = get_details(self.id_disease)
        self.treatments = get_treatments_details(self.id_disease)
        print(self.disease_details)
        print(self.treatments)

    def get_id_disease(self):
        return self.id_disease

    def get_disease_details(self):
        return self.disease_details

    def get_treatments(self):
        return self.treatments


if __name__ == "__main__":
    app.run()
