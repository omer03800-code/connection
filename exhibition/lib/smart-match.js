// Smart matching engine — finds likely connections for a new person
// based on shared city, field, community tags, and mutual friends.

// Maps raw tag/role/description keywords → canonical field labels
const FIELD_KEYWORDS = {
    design:      ['design', 'designer', 'visual communication', 'תקשורת חזותית', 'graphic', 'ui', 'ux', 'industrial design', 'bezalel', 'wix'],
    tech:        ['hi-tech', 'hitech', 'software', 'developer', 'engineer', 'cto', 'startup', 'cyber', 'programming', 'קוד'],
    law:         ['law', 'lawyer', 'legal', 'attorney', 'עורך דין', 'עורכת דין'],
    medicine:    ['doctor', 'nurse', 'medical', 'health', 'physician', 'רופא', 'אחות', 'רפואה'],
    education:   ['teacher', 'education', 'מורה', 'חינוך', 'teaching', 'special education'],
    finance:     ['finance', 'pension', 'accounting', 'accountant', 'fintech', 'investment', 'כלכלה', 'רואה חשבון'],
    media:       ['journalist', 'reporter', 'tv', 'film', 'production', 'media', 'news', 'עיתונאי', 'עיתונאית'],
    music:       ['music', 'singer', 'musician', 'producer', 'concert', 'מוזיקה', 'זמר', 'זמרת'],
    sports:      ['football', 'soccer', 'sport', 'athlete', 'goalkeeper', 'כדורגל', 'ספורט'],
    psychology:  ['psychology', 'therapist', 'psychologist', 'social work', 'פסיכולוג', 'עבודה סוציאלית'],
    fashion:     ['fashion', 'stylist', 'clothing', 'אופנה', 'סטייליסט'],
    hr:          ['hr', 'human resources', 'recruitment', 'גיוס', 'משאבי אנוש'],
    fitness:     ['fitness', 'pilates', 'trainer', 'gym', 'כושר', 'פילאטיס'],
    real_estate: ['real estate', 'נדל"ן', 'realty'],
    diamonds:    ['diamond', 'יהלומים'],
    marketing:   ['marketing', 'advertising', 'brand', 'שיווק', 'פרסום'],
};

// Maps tag strings → human-readable community label
const COMMUNITY_LABELS = {
    '#HaifaUniversity':  'לומד/ת באוניברסיטת חיפה',
    '#KadoorieSchool':   'בוגר/ת תיכון כדורי',
    '#Ilaniya':          'קשור/ה למושב אילניה',
    '#Pikud':            'שירת/שירתה בפיקוד העורף',
    '#NoadrTeam':        'חבר/ה בצוות נועדר',
    '#BayernMunich':     'קשור/ה לבאיירן מינכן',
    '#KibbutzErez':      'קשור/ה לקיבוץ ארז',
    '#BeitKeshet':       'קשור/ה לקיבוץ בית קשת',
    '#Bezalel':          'לומד/ת בבצלאל',
    '#Wix':              'עובד/ת בוויקס',
    '#Elbit':            'עובד/ת באלביט',
    '#MilitaryIntelligence': 'שירת/שירתה במודיעין',
    '#Unit669':          'שירת/שירתה ביחידה 669',
    '#AirForce':         'שירת/שירתה בחיל האוויר',
    '#Golani':           'שירת/שירתה בגולני',
    '#ArmoredCorps':     'שירת/שירתה בשריון',
};

function extractFields(profile) {
    const text = [
        profile.role || '',
        profile.description || '',
        profile.tags || '',
    ].join(' ').toLowerCase();

    return Object.entries(FIELD_KEYWORDS)
        .filter(([, keywords]) => keywords.some(kw => text.includes(kw)))
        .map(([field]) => field);
}

function extractTags(profile) {
    if (!profile.tags) return [];
    return profile.tags.split(',').map(t => t.trim()).filter(Boolean);
}

function normalizeCity(city) {
    if (!city) return null;
    return city.toLowerCase()
        .replace(/^tel aviv.*/, 'tel aviv')
        .replace(/^haifa.*/, 'haifa')
        .replace(/^jerusalem.*/, 'jerusalem')
        .replace(/^moshav ilaniya.*/, 'moshav ilaniya')
        .trim();
}

function ageGroup(age) {
    const n = parseInt(age);
    if (!n) return null;
    return Math.floor(n / 5) * 5; // groups: 20, 25, 30...
}

/**
 * Given a candidate profile (not yet in DB), suggest likely connections from existing people.
 *
 * @param {object} candidate - { name, age, city, role, description, tags }
 * @param {object[]} allPeople - all existing people from DB
 * @param {number[]} existingConnectionIds - IDs already manually connected by the user
 * @param {object} adjacencyMap - { [personId]: number[] } for mutual-friend scoring
 * @returns {{ person: object, score: number, reasons: string[] }[]}
 */
function suggestConnections(candidate, allPeople, existingConnectionIds = [], adjacencyMap = {}) {
    const existingSet = new Set(existingConnectionIds);
    const candidateFields = extractFields(candidate);
    const candidateTags = extractTags(candidate);
    const candidateCity = normalizeCity(candidate.city);
    const candidateAgeGroup = ageGroup(candidate.age);

    const scored = [];

    for (const person of allPeople) {
        if (existingSet.has(person.id)) continue;
        if (person.name === candidate.name) continue;

        const reasons = [];
        let score = 0;

        // 1. Same city
        const personCity = normalizeCity(person.city);
        if (candidateCity && personCity && candidateCity === personCity) {
            score += 3;
            reasons.push(`שניכם מ${person.city}`);
        }

        // 2. Shared community tags
        const personTags = extractTags(person);
        for (const tag of candidateTags) {
            if (personTags.includes(tag) && COMMUNITY_LABELS[tag]) {
                score += 5;
                reasons.push(COMMUNITY_LABELS[tag]);
            }
        }

        // 3. Shared field of work/study
        const personFields = extractFields(person);
        const sharedFields = candidateFields.filter(f => personFields.includes(f));
        if (sharedFields.length > 0) {
            score += sharedFields.length * 3;
            const fieldLabels = { design:'עיצוב', tech:'הייטק', law:'משפטים', medicine:'רפואה', education:'חינוך', finance:'פיננסים', media:'מדיה', music:'מוזיקה', sports:'ספורט', psychology:'פסיכולוגיה', fashion:'אופנה', hr:'משאבי אנוש', fitness:'כושר', real_estate:'נדלן', marketing:'שיווק' };
            sharedFields.forEach(f => {
                if (fieldLabels[f]) reasons.push(`שניכם בתחום ${fieldLabels[f]}`);
            });
        }

        // 4. Similar age bracket
        const personAgeGroup = ageGroup(person.age);
        if (candidateAgeGroup && personAgeGroup && candidateAgeGroup === personAgeGroup) {
            score += 1;
        }

        // 5. City + field combo bonus (stronger signal)
        if (candidateCity && personCity && candidateCity === personCity && sharedFields.length > 0) {
            score += 4;
        }

        // 6. Mutual connections (friends of friends)
        if (adjacencyMap[person.id]) {
            const mutuals = adjacencyMap[person.id].filter(id => existingSet.has(id));
            if (mutuals.length > 0) {
                score += Math.min(mutuals.length * 2, 10);
                reasons.push(`${mutuals.length} חבר/ה משותף/ים`);
            }
        }

        if (score >= 3 && reasons.length > 0) {
            scored.push({ person, score, reasons: [...new Set(reasons)] });
        }
    }

    return scored
        .sort((a, b) => b.score - a.score)
        .slice(0, 8);
}

module.exports = { suggestConnections, extractFields, extractTags };
