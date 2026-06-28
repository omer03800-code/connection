const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf8');

const calcMatchScoreStr = html.substring(html.indexOf('function calculateMatchScore'), html.indexOf('function generateRecommendations'));
eval(calcMatchScoreStr);

const p1 = {
    age: '',
    city: '',
    originCity: '',
    role: '',
    description: "moshav ilania, kadoorie, sambatzit, haifa university, visual communication",
    tags: []
};

const yotam = {
    id: 2,
    name: 'Yotam Lerman',
    city: 'Tel Aviv',
    role: 'Industrial Engineering & Management student',
    tags: '#Friend,highschool:Kadoorie School,#Ilaniya #openuiversty,#TelAviv,#IndustrialEngineering&Management—OpenUniversity,#moshavilaniya,#ilaniya,#paratroopers,#tzanhanim,#elal,#combatsoldier,#openuniversity,#IndustrialEngineering&Managementstudent'
};

const shani = {
    id: 19,
    name: 'Shani Libner',
    city: 'Ramat Gan',
    role: 'Designer at Wix | Visual Communication student — Haifa university',
    tags: '#Friend,education:Haifa University,education:Visual Communication,#Wix,#Designer,#RamatGan,#DesigneratWix|VisualCommunicationstudent—Haifa,#education,#educationnco,#mashakitchinuch'
};

const ignoreCities = ['tel aviv', 'jerusalem', 'haifa', 'תל אביב', 'ירושלים', 'חיפה'];

console.log("Yotam:", calculateMatchScore(p1, yotam));
console.log("Shani:", calculateMatchScore(p1, shani));

