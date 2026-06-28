const dbData = [
  { name: 'Maayan Hershler', city: 'Moshav Ilania', role: 'Accountant', tags: '#Ilania', description: 'Work at Raffael', age: '30' }
];

const synonymGroups = [
  { type: 'small_town', words: ['ilaniya', 'ilania', 'ilanya', 'illania', 'אילניה', 'מושב אילניה', 'אילנייה'] }
];

const p1 = {
  city: 'Ilania',
  originCity: '',
  role: '',
  description: '',
  tags: '',
  age: ''
};

const p1Text = ' ' + [(p1.city||'').toLowerCase(), (p1.originCity||'').toLowerCase(), (p1.role||'').toLowerCase(), (p1.description||'').toLowerCase()].join(' ').replace(/[,.!]/g, ' ') + ' ';

let activeGroups = [];
synonymGroups.forEach((group, idx) => {
    if (group.words.some(word => p1Text.includes(' ' + word + ' '))) {
        activeGroups.push({ idx: idx, type: group.type });
    }
});

let score = 0;
const p2 = dbData[0];
const p2TagsCleaned = (p2.tags || '').replace(/#/, '').split(',');
const p2Text = ' ' + [(p2.city||'').toLowerCase(), (p2.originCity||'').toLowerCase(), (p2.role||'').toLowerCase(), (p2.description||'').toLowerCase(), ...p2TagsCleaned].join(' ').replace(/[,.!]/g, ' ') + ' ';

let shared = { uni: 0, degree: 0, company: 0, big_city: 0, small_town: 0, army_unit: 0, army_base: 0, high_school: 0, mechina: 0 };

activeGroups.forEach(ag => {
    if (synonymGroups[ag.idx].words.some(word => p2Text.includes(' ' + word + ' '))) {
        shared[ag.type]++;
    }
});

console.log("p1Text:", p1Text);
console.log("p2Text:", p2Text);
console.log("activeGroups:", activeGroups);
console.log("shared:", shared);
