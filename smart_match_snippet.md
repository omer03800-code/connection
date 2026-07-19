```javascript
// Smart matching engine — finds likely connections for a new person
// based on shared city, field, community tags, and mutual friends.

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

// Niche fields that grant connection points if in the same city
const NICHE_FIELDS = ['media', 'music', 'sports', 'psychology', 'fashion', 'hr', 'fitness', 'real_estate', 'diamonds', 'marketing'];

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

const WORKPLACE_TAGS = ['#Wix', '#Elbit']; 
const AGE_DEPENDENT_TAGS = ['#KadoorieSchool', '#Pikud', '#Unit669', '#Golani', '#ArmoredCorps', '#AirForce', '#MilitaryIntelligence', '#NoadrTeam', '#BayernMunich', '#KibbutzErez', '#BeitKeshet', '#Bezalel'];
const UNIVERSITY_TAGS = ['#HaifaUniversity'];

// In-memory cache for computed traits to save O(N) regex and string checks on every request
const personTraitsCache = new Map();

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

function isLecturer(profile) {
    const role = (profile.role || '').toLowerCase();
    const desc = (profile.description || '').toLowerCase();
    return role.includes('lecturer') || role.includes('מרצה') || desc.includes('lecturer') || desc.includes('מרצה');
}

function getPersonTraits(person) {
    // Return cached traits if available to reduce time complexity to O(1) per person
    if (person.id && personTraitsCache.has(person.id)) {
        return personTraitsCache.get(person.id);
    }
    
    const tags = extractTags(person);
    const fields = extractFields(person);
    const age = parseInt(person.age) || null;
    const city = normalizeCity(person.city);
    const isLec = isLecturer(person);
    
    // Extract last name (only if the name has more than 1 word)
    let lastName = null;
    if (person.name) {
        const parts = person.name.trim().split(/\s+/);
        if (parts.length > 1) {
            lastName = parts[parts.length - 1].toLowerCase();
        }
    }
    
    const traits = { tags, fields, age, city, lastName, isLec };
    if (person.id) personTraitsCache.set(person.id, traits);
    return traits;
}

/**
 * Given a candidate profile (not yet in DB), suggest likely connections from existing people.
 */
function suggestConnections(candidate, allPeople, existingConnectionIds = [], adjacencyMap = {}) {
    const existingSet = new Set(existingConnectionIds);
    const candTraits = getPersonTraits(candidate);
    
    const scored = [];

    for (const person of allPeople) {
        if (existingSet.has(person.id)) continue;
        if (person.name === candidate.name) continue;

        const pTraits = getPersonTraits(person);
        const reasons = [];
        let score = 0;

        // 1. Same workplace (No age dependence)
        for (const tag of candTraits.tags) {
            if (WORKPLACE_TAGS.includes(tag) && pTraits.tags.includes(tag)) {
                score += 5;
                const companyName = tag.replace('#', '');
                reasons.push(`שניכם עובדים/עבדתם ב-${companyName}`);
            }
        }

        // 2. Age-dependent tags (Army, High school) - Max age gap 3 years
        const ageGap = (candTraits.age && pTraits.age) ? Math.abs(candTraits.age - pTraits.age) : null;
        
        if (ageGap !== null && ageGap <= 3) {
            for (const tag of candTraits.tags) {
                if (AGE_DEPENDENT_TAGS.includes(tag) && pTraits.tags.includes(tag)) {
                    score += 6;
                    reasons.push(`שירתתם/למדתם יחד (${COMMUNITY_LABELS[tag] || tag})`);
                }
            }
        }

        // 3. University + Field combo (Max age gap 5 years, UNLESS one is a lecturer)
        if (ageGap !== null) {
            const isUniAgeGapValid = ageGap <= 5 || candTraits.isLec || pTraits.isLec;
            
            if (isUniAgeGapValid) {
                const sharedUni = candTraits.tags.find(t => UNIVERSITY_TAGS.includes(t) && pTraits.tags.includes(t));
                const sharedField = candTraits.fields.find(f => pTraits.fields.includes(f));
                
                if (sharedUni && sharedField) {
                    score += 5;
                    if (candTraits.isLec || pTraits.isLec) {
                        reasons.push("סגל וסטודנטים מאותו חוג באוניברסיטה");
                    } else {
                        reasons.push("למדתם אותו חוג באוניברסיטה באותן שנים");
                    }
                }
            }
        }

        // 4. Niche profession in the same city
        if (candTraits.city && pTraits.city && candTraits.city === pTraits.city) {
            const sharedNiche = candTraits.fields.find(f => NICHE_FIELDS.includes(f) && pTraits.fields.includes(f));
            if (sharedNiche) {
                score += 5;
                reasons.push("שניכם מאותה העיר ועוסקים בתחום דומה");
            }
        }

        // 5. Same last name (Family circles)
        if (candTraits.lastName && pTraits.lastName && candTraits.lastName === pTraits.lastName) {
            score += 6;
            reasons.push("חולקים את אותו שם משפחה");
        }

        // 6. Mutual connections
        if (adjacencyMap[person.id]) {
            const mutuals = adjacencyMap[person.id].filter(id => existingSet.has(id));
            if (mutuals.length > 0) {
                score += Math.min(mutuals.length * 3, 15); // +3 points per mutual friend, capped at 15
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
```
