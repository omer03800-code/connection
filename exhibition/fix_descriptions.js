const { getDb } = require('./db/schema');
const db = getDb();

const updates = [
  { name: "Or Hogi", tags: "community:Ashkelon" },
  { name: "Idan Barak", tags: "community:Ilania,other:Twin of Omer" },
  { name: "Shani Libner", tags: "community:Kiryat Haim,military:IDF dental assistant" },
  { name: "Noya Ma'or", tags: "community:Hadera / Shamshit / Tiv'on,military:Sky Rider simulator instructor" },
  { name: "Re'ut Brikenstein", tags: "community:Zichron Ya'akov,highschool:Keshet Democratic,military:Nahal Nucleus / Soldier-teacher" },
  { name: "Oral Shafsha", tags: "community:Netanya,highschool:ORT Leibowitz,military:Unit 81" },
  { name: "Hila Ben Shabbat", tags: "community:Kiryat Motzkin,military:Military Intelligence Graphic Designer" },
  { name: "Shachar Liz Ben Or", tags: "community:Kfar Yona,military:IDF Spokesperson,highschool:Rigler" },
  { name: "Shuki Weiss", tags: "community:Moshav Ilaniya,workplace:Music Producer" },
  { name: "Guy Oseary", tags: "workplace:Maverick President,other:Madonna Manager" },
  { name: "Avner Netanyahu", tags: "education:Hebrew University,other:Friend of Ben Bronshtein" },
  { name: "Benjamin Netanyahu", tags: "education:MIT,military:Sayeret Matkal" },
  { name: "Shai Avgi", tags: "community:Eilat,highschool:Goldwater,education:Seminar HaKibbutzim (B.Ed),workplace:Teacher at Tikhonit TLV" },
  { name: "Daniel Harari", tags: "highschool:Mevo'ot HaNegev,workplace:Fitness coach & Israel Railways" },
  { name: "Gili Zanzuri", tags: "community:Re'ut,highschool:Mor,workplace:Advertising agency" },
  { name: "Amit Bashiri", tags: "community:Kfar Vardim,highschool:Manor Kabri,workplace:Pilates instructor,military:Mashakit Chinuch" },
  { name: "Liat Malach", tags: "community:Gedera" },
  { name: "Lital Ashel", tags: "other:Wife of Lior Ashel" },
  { name: "Dana Rik Ashel", tags: "other:Wife of Ben Ashel" },
  { name: "Noam", tags: "other:Husband of Ariel Bronshtein" },
  { name: "Omer Barak", tags: "community:Ilania,highschool:Kadoorie,youth:Derech Eretz - Nitzana,military:Sambatzit" },
  { name: "Lihi Dahan", tags: "community:Ma'ale Adumim,highschool:Hadera" },
  { name: "Shahar Arbiv", tags: "community:Hod HaSharon,highschool:Ramon,workplace:Law firm" },
  { name: "Shai Rosenberg", tags: "community:Kibbutz Erez,highschool:Sha'ar HaNegev,youth:Derech Eretz - Nitzana" },
  { name: "Rotem Dahan", tags: "community:Modi'in,highschool:Ironi Bet,education:Ariel University,workplace:RiseUp,military:Givati Combat Soldier" },
  { name: "Marito Amara", tags: "education:Ono Academy,youth:Derech Eretz - Nitzana" },
  { name: "shani hanania", tags: "community:Binyamina" },
  { name: "Neta Port ", tags: "community:Mazkeret Batya,education:Kiryat Ono,youth:Nachshon" },
  { name: "Amir Katz", tags: "community:Ramat Gan & Kfar Sirkin" },
  { name: "Nofar Mishali ", tags: "education:Bezalel,workplace:Fashion Designer at Fox" },
  { name: "Ran David", tags: "community:Timorim Moshav,highschool:Be'er Tuvia,military:Golani Brigade,education:Afeka College" },
  { name: "Shaked Klettr", tags: "community:Kiryat Motzkin,highschool:Migdal HaEmek,military:Combat Engineering Corps" },
  { name: "Yuval Cohen", tags: "community:Tel Aviv,education:Bar-Ilan University,highschool:Alliance,military:Nahal Reconnaissance Unit" },
  { name: "Tomer Sela", tags: "community:Moshav Timorim,education:Netanya Academic College,highschool:Be'er Tuvia,military:Artillery Corps" },
  { name: "Ronit Izraeli", tags: "community:Ayelet HaShachar,highschool:Emek Hula,education:Bezalel Academy,workplace:Graphic Designer & Lecturer" }
];

const stmt = db.prepare("UPDATE people SET tags = tags || ?, description = '' WHERE name = ?");
const getStmt = db.prepare("SELECT tags FROM people WHERE name = ?");

for (const u of updates) {
  const row = getStmt.get(u.name);
  if (row) {
    stmt.run("," + u.tags, u.name);
    console.log(`Updated ${u.name}`);
  }
}
console.log("Done!");
