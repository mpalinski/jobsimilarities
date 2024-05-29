from flask import Flask, request, render_template, render_template_string, session
from markupsafe import escape
import pandas as pd
import json
import secrets
from collections import Counter
from whitenoise import WhiteNoise

# secret=secrets.token_hex(16)
secret='AAAASDFSVRVRG6532AFBR'

app = Flask(__name__)
app.config['SECRET_KEY']=secret

# app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")

df=pd.read_json('static/db_jobs.json')
jobDict=df['job'].to_dict()
dfMap=pd.read_csv('static/jobDemand.csv')
dfDesc=pd.read_csv('static/jobDesc.csv')

def is_nested_list(obj):
    if not isinstance(obj, list):
        return False
    for item in obj:
        if isinstance(item, list):
            return True
    return False


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html', msg=jobDict)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html', msg=jobDict)

@app.route("/sessionClear")
def sessionClear():
    session.pop('regionClick',None)
    return render_template('amchartsMapSelect.html')

@app.route("/mapClick/<userinfo>", methods=['GET', 'POST'])
def ProcessUserinfo(userinfo):
    regionClick=json.loads(userinfo)
    if 'regionClick' not in session:
        session['regionClick'] = []  
    region_list = session['regionClick']
    if type(regionClick) == list:
      region_list.extend(regionClick)
    elif type(regionClick) == str:
      region_list.extend([regionClick])
    else:
      print('err')
    session['regionClick'] = region_list    
    # print(session['regionClick'])
    return('/') 

@app.route("/select", methods=['GET', 'POST'])
def select():   
    templ='''
    <div class="blob red">4</div>
    Najedź na zawód, by sprawdzić zapotrzebowanie
</br>
    <div class="blob red">5</div>
    Kliknij zawód, żeby przeczytać jego opis

<hr>
        <table id="dataTable" class="table table-borderless">
        <thead>
        <tr>

        <th>
        <a class="headerPointer" data-toggle="modal" data-target=".bd-example-modal-lg">Dopasowanie </a>
        </th>

        
        <th>
        Zawód 
        </th>

        <th class='delCol'>
        </th>

  <th>
        </th>

        </tr>

       

        </thead>
        <tbody>
    {% for index,row in job_info.iterrows() %}
            <tr>
            <td class="align-middle">
                <div class="progress" style="width: 100px;" >
                <div class="progress-bar" role="progressbar" aria-label="Example with label" style="{{ "width:" ~ row['similarityIndex'] ~ "%;" ~ "background-color: #2f90a8" }}" aria-valuenow="{{ row['similarityIndex'] }}" aria-valuemin="0" aria-valuemax="100">{{ row['similarityIndex'] }}
                </div>
                </div>
            </td>
          
            <td class="align-middle"> 
                <p class="highlight">   
                <a name="jobClick" id="{{ row['jobCode'] }}" hx-post="/mapUpdate"
                hx-trigger="mouseenter delay:.3s"
                hx-target="#mapHeatDiv" 
                href="#" data-toggle="modal" data-target=".{{ row['jobCode'] }}"> {{ row['similarJobs'] }}
                </a>
                </p>
            </td>

             <td>
             <span class="material-symbols-outlined remove">
              delete_forever
            </span>
            </td>

            <td>
            {{ row['synteza'] }}
            </td>

            </tr>
        {% endfor %}
        </tbody>
  </table>



<script>
    $(document).ready(function() {
        // Initialize DataTables
        $('#dataTable').DataTable({
            "responsive": true,
            "lengthChange": false,
            "pageLength": 5,
            "searching": false,
            "ordering": false,
            "info": false,
            "paging": true,
      dom: 'frtiBp',

      columns: [
      { title: 'Dopasowanie', data: 'dopasowanie' },
      { title: 'Zawód', data: 'zawód' },
      { title: '', data: 'delete' },
      { title: 'Opis zawodu', data: 'synteza', visible: false }
    ],
      buttons: [
      {
        extend: 'excel',
        title: null,
        filename:"podobne_zawody",
        exportOptions: {
            columns: 'th:not(:last-child)'
         }
      }
    ]
    
        });

$('#dataTable').on('click', '.remove', function () {
		var table = $('#dataTable').DataTable();
		table
			.row($(this).parents('tr'))
			.remove()
		.draw();
		});

      
 // Event handler for page change
    $('#dataTable_wrapper').on('click', function() {
        onPageChange();
    });

    // Function to perform an action when the page changes
    function onPageChange() {
        console.log('Page has been changed!');
        // Add your custom code here
              htmx.process("#dataTable_wrapper");

    }

    });



      htmx.process("#dataTable_wrapper");

</script>

<div class="story-content">

<button class="btn btn-link"> 
  <div class="story-btn"> 
      <a href="#wybor"> Powrót </a>
 </div>
   </button>
   |
   <button class="btn btn-link"> 
  <div class="story-btn"> 
      <a href="#metody"> Metodologia </a>
 </div>
   </button>
   </div>

<div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
 <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Indeks podobieństwa</h5>
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>
         Indeks odzwierciedla podobieństwo prezentowanych zawodów z obecnie wykonywanym przez Pana/ią zawodem/ami. Indeks może przyjmować wartości od 0 do 100, im wyższa wartość, tym zawody są bardziej do siebie podobne pod kątem wymaganych umiejętności i wykonywanych w ich ramach zadań. Indeks obliczamy przy pomocy metod z zakresu uczenia maszynowego (Latent Semantic Analysis). Więcej o naszej metodologii możesz przeczytać tu: <a href="#metody">metodologia</a>. 
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-link" data-dismiss="modal">Zamknij</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade bd-money-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
 <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Wynagrodzenie</h5>
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>
    Wynagrodzenie prezentujemy jako medianę raportowanych wynagrodzeń w badaniu BAEL 2020 i w Październikowym Badaniu Wynagrodzeń 2020 przeprowadzanych przez GUS. Mediana, to inaczej wartość środkowa, tzn. 50% osób w danym zawodzie zarabia powyżej tej wartości i kolejne 50% powyżej niej. W przypadku wynagrodzeń uważa się, że mediana pokazuje prawdziwszy obraz niż średnia, ponieważ jest mniej wrażliwa na odstające obserwacje.
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-link" data-dismiss="modal">Zamknij</button>
      </div>
    </div>
  </div>
</div>


{% for index,row in job_info.iterrows() %}

<div class="modal fade {{ row['jobCode'] }}" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
 <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ row['similarJobs'] }}</h5>
        </button>
      </div>
      <div class="modal-body">
        <p style="text-align: justify">
     
    {{ row['synteza'] }}

        </p>
        <hr>
</br>
       <p>
      Mediana wynagrodzenia netto w 2020 roku: {{ row['medianWage'] }} zł
      </p> 
      <p> Źródło danych o wynagrodzeniach: GUS Z-12, BAEL </p>

<hr>
      </br>
      <p> Grupa wielka klasyfikacji: {{ row['groupLarge'] }} </p>      
      <p>
        Najbardziej odpowiedni poziom wykształcenia: {{ row['eduLevel'] }}
      </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-link">
        <a href="{{ 'https://psz.praca.gov.pl/rynek-pracy/bazy-danych/klasyfikacja-zawodow-i-specjalnosci/wyszukiwarka-opisow-zawodow//-/klasyfikacja_zawodow/zawod/' + row['jobCodeStr'] }}" target="_blank">
        Czytaj więcej
        </a>
        </button>
      |
        <button type="button" class="btn btn-link" data-dismiss="modal">Zamknij</button>
      </div>
    </div>
  </div>
</div>



{% endfor %}

<script>
$(".buttons-excel span").text("Drukuj raport");
</script>
    '''    


    jobIndex=request.form.getlist('states[]')
    jobIndex=[int(i) for i in jobIndex]
    jobInfo=df[df.index.isin(jobIndex)]
    jobInfo=jobInfo.set_index(['job','jobPotential']).apply(pd.Series.explode).reset_index()
    jobInfo['similarityIndex']=jobInfo['similarityIndex'].astype(int)
    jobName=jobInfo['job'].unique()

    if len(jobIndex)==1:
        jobInfo=jobInfo.sort_values(['job','similarityIndex','jobCode'],ascending=False).groupby(['job','jobPotential'])['similarJobs','similarityIndex','medianWage','jobPotential','jobCode'].head(15)
        jobInfo=jobInfo.groupby(['similarJobs','jobPotential','medianWage','jobCode']).mean().reset_index().sort_values('similarityIndex',ascending=False)
        jobInfo[['medianWage','similarityIndex']]=jobInfo[['medianWage','similarityIndex']].astype(int)
        jobInfo['medianWage']=jobInfo['medianWage'].replace(0,"Brak danych")
        jobInfo['jobCode']=jobInfo['jobCode'].astype(int)
        jobInfo=jobInfo.merge(dfDesc,on='jobCode')
        jobInfo['jobCodeStr']=jobInfo['jobCode'].astype(str)
        jobInfo['edu']=jobInfo['jobCodeStr'].str[0]
        jobInfo['groupLarge']=jobInfo['edu'].str[0].map({'1':'Przedstawiciele władz publicznych, wyżsi urzędnicy i kierownicy',
                                  '2':'Specjaliści',
                                 '3':'Technicy i inny średni personel',
                                 '4':'Pracownicy biurowi',
                                 '5':'Pracownicy usług osobistych i sprzedawcy',
                                 '6':'Rolnicy, ogrodnicy, leśnicy i rybacy',
                                 '7':'Robotnicy przemysłowi i rzemieślnicy',
                                 '8':'Operatorzy i monterzy maszyn i urządzeń',
                                 '9':'Pracownicy przy pracach prostych'})
        jobInfo['eduLevel']=jobInfo['edu'].str[0].map({'1':'wyższe',
                                  '2':'wyższe',
                                 '3':'techniczne/policealne',
                                 '4':'średnie',
                                 '5':'średnie',
                                 '6':'średnie',
                                 '7':'średnie',
                                 '8':'średnie',
                                 '9':'podstawowe'})

    elif len(jobIndex)==2:
        jobInfo=jobInfo.sort_values(['job','similarityIndex','jobCode'],ascending=False).groupby(['job','jobPotential'])['similarJobs','similarityIndex','medianWage','jobPotential','jobCode'].head(7)
        jobInfo=jobInfo.groupby(['similarJobs','jobPotential','medianWage','jobCode']).mean().reset_index().sort_values('similarityIndex',ascending=False)
        jobInfo[['medianWage','similarityIndex']]=jobInfo[['medianWage','similarityIndex']].astype(int)
        jobInfo['medianWage']=jobInfo['medianWage'].replace(0,"Brak danych")
        jobInfo['jobCode']=jobInfo['jobCode'].astype(int)
        jobInfo=jobInfo.merge(dfDesc,on='jobCode')
        jobInfo['jobCodeStr']=jobInfo['jobCode'].astype(str)
        jobInfo['edu']=jobInfo['jobCodeStr'].str[0]
        jobInfo['groupLarge']=jobInfo['edu'].str[0].map({'1':'Przedstawiciele władz publicznych, wyżsi urzędnicy i kierownicy',
                                  '2':'Specjaliści',
                                 '3':'Technicy i inny średni personel',
                                 '4':'Pracownicy biurowi',
                                 '5':'Pracownicy usług osobistych i sprzedawcy',
                                 '6':'Rolnicy, ogrodnicy, leśnicy i rybacy',
                                 '7':'Robotnicy przemysłowi i rzemieślnicy',
                                 '8':'Operatorzy i monterzy maszyn i urządzeń',
                                 '9':'Pracownicy przy pracach prostych'})
        jobInfo['eduLevel']=jobInfo['edu'].str[0].map({'1':'wyższe',
                                  '2':'wyższe',
                                 '3':'techniczne/policealne',
                                 '4':'średnie',
                                 '5':'średnie',
                                 '6':'średnie',
                                 '7':'średnie',
                                 '8':'średnie',
                                 '9':'podstawowe'})
    elif len(jobIndex)==3:
        jobInfo=jobInfo.sort_values(['job','similarityIndex','jobCode'],ascending=False).groupby(['job','jobPotential'])['similarJobs','similarityIndex','medianWage','jobPotential','jobCode'].head(5)
        jobInfo=jobInfo.groupby(['similarJobs','jobPotential','medianWage','jobCode']).mean().reset_index().sort_values('similarityIndex',ascending=False)
        jobInfo[['medianWage','similarityIndex']]=jobInfo[['medianWage','similarityIndex']].astype(int)
        jobInfo['medianWage']=jobInfo['medianWage'].replace(0,"Brak danych")
        jobInfo['jobCode']=jobInfo['jobCode'].astype(int)
        jobInfo=jobInfo.merge(dfDesc,on='jobCode')
        jobInfo['jobCodeStr']=jobInfo['jobCode'].astype(str)
        jobInfo['edu']=jobInfo['jobCodeStr'].str[0]
        jobInfo['groupLarge']=jobInfo['edu'].str[0].map({'1':'Przedstawiciele władz publicznych, wyżsi urzędnicy i kierownicy',
                                  '2':'Specjaliści',
                                 '3':'Technicy i inny średni personel',
                                 '4':'Pracownicy biurowi',
                                 '5':'Pracownicy usług osobistych i sprzedawcy',
                                 '6':'Rolnicy, ogrodnicy, leśnicy i rybacy',
                                 '7':'Robotnicy przemysłowi i rzemieślnicy',
                                 '8':'Operatorzy i monterzy maszyn i urządzeń',
                                 '9':'Pracownicy przy pracach prostych'})
        jobInfo['eduLevel']=jobInfo['edu'].str[0].map({'1':'wyższe',
                                  '2':'wyższe',
                                 '3':'techniczne/policealne',
                                 '4':'średnie',
                                 '5':'średnie',
                                 '6':'średnie',
                                 '7':'średnie',
                                 '8':'średnie',
                                 '9':'podstawowe'})
    else:
        print('Too many jobs selected')
        
    return render_template_string(templ, job_info=jobInfo, job_names=jobName)

@app.route("/mapUpdate", methods=['GET', 'POST'])
def mapUpdate():
    print('started')
    regions_ID = session.get('regionClick', None)
    # session['regionClick'] = []  

    print(regions_ID)
    # odd number means region is selected
    c=Counter(regions_ID)
    regionsSel=[]
    for it in c.items():
        if it[1]%2!=0:
            regionsSel.append(it[0])
        else:
            pass
    # print(regionsSel)
    job_ID=request.headers.get('HX-Trigger')
    tmp=dfMap[(dfMap['code']==int(job_ID)) & (dfMap['region'].isin(regionsSel))]
    # print(tmp)
    demand_data=[
      {
        "name": "nadwyżka",
        "color": "#77c7ff",
        "data": []
      },
      {
        "name": "równowaga",
        "color": "#c3cad8",
        "data": []
      },
      {
        "name": "deficyt",
        "color": "#ee8308",
        "data": []
      },
      {
        "name": "brak danych",
        "color": "#f2f2f2",
        "data": []
      }
    ]

    keys=['title', 'customData', 'groupId','id']

    for idx,situation in enumerate([1,0,-1,2]):
        data=[]
        # for r in tmp[tmp['jobDemand']==situation]['region']:
        for no,row in tmp[tmp['jobDemand']==situation].iterrows():
            di={}
            values=['', situation, '',row['id']]
            for i in range(len(keys)):
                di[keys[i]]=values[i]
            data.append(di)
        demand_data[idx]['data']=data

    # print(demand_data)

    job_name=dfDesc[dfDesc['jobCode']==int(job_ID)]['nazwa_zawodu'].values[0]

    return render_template('amchartsMapHeat.html', jobID=job_ID, demandData=demand_data, jobName=job_name)

if __name__ == "__main__":
    app.run(debug=True)