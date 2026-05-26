"""
python manage.py add_local_docs

Adds sample documents in Amharic, Tigrinya, and Afan Oromo
so that searching in those languages returns real results.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from search.models import Document


DOCS = [
    # ── AMHARIC ──────────────────────────────────────────────────────────
    {
        'title': 'መረጃ ፍለጋ ምንድን ነው',
        'language': 'amharic',
        'raw_text': (
            'መረጃ ፍለጋ ማለት ከሰነዶች ስብስብ ውስጥ ተዛማጅ መረጃ የማግኘት ሂደት ነው። '
            'ፍለጋ ሞተሮች የጽሑፍ ሰነዶችን ለማደራጀት እና ለማስፈለግ ይጠቀማሉ። '
            'ቁልፍ ቃላት ፍለጋ፣ ቬክተር ቦታ ሞዴል እና BM25 ዋና ዋና ዘዴዎች ናቸው። '
            'ኢንዴክሲንግ ሰነዶችን ፈጣን ፍለጋ ለማድረግ ያስችላል።'
        ),
    },
    {
        'title': 'ቬክተር ቦታ ሞዴል',
        'language': 'amharic',
        'raw_text': (
            'ቬክተር ቦታ ሞዴል ሰነዶችን እና ጥያቄዎችን እንደ ቬክተሮች ይወክላል። '
            'ኮሳይን ተመሳሳይነት ሁለት ቬክተሮች ምን ያህል ቅርብ እንደሆኑ ይለካል። '
            'TF-IDF ክብደት ቃላቱ ምን ያህል አስፈላጊ እንደሆኑ ያሳያል። '
            'ይህ ሞዴል በዘመናዊ ፍለጋ ሞተሮች ውስጥ ሰፊ አጠቃቀም አለው።'
        ),
    },
    {
        'title': 'ኢትዮጵያ ታሪክ እና ባህል',
        'language': 'amharic',
        'raw_text': (
            'ኢትዮጵያ በምስራቅ አፍሪካ የምትገኝ ጥንታዊ ሀገር ናት። '
            'አማርኛ የኢትዮጵያ ብሔራዊ ቋንቋ ሲሆን ከ100 ሚሊዮን በላይ ሰዎች ይናገሩታል። '
            'አክሱም፣ ላሊበላ እና ጎንደር ታሪካዊ ከተሞች ናቸው። '
            'ኢትዮጵያ ቡና የተወለደባት ሀገር ናት።'
        ),
    },
    {
        'title': 'ቴክኖሎጂ እና ሳይንስ',
        'language': 'amharic',
        'raw_text': (
            'ሰው ሰራሽ አስተውሎት ዘመናዊ ቴክኖሎጂ ዋና አካል ሆኗል። '
            'ማሽን ለርኒንግ ኮምፒዩተሮች ከውሂብ እንዲማሩ ያስችላቸዋል። '
            'ተፈጥሯዊ ቋንቋ ሂደት ኮምፒዩተሮች ቋንቋን እንዲረዱ ይረዳቸዋል። '
            'ዲጂታል ቴክኖሎጂ ትምህርት፣ ጤና እና ንግድን ለውጧል።'
        ),
    },
    {
        'title': 'ጤና እና ህክምና',
        'language': 'amharic',
        'raw_text': (
            'ጤናማ ህይወት ለመኖር ምግብ፣ ስፖርት እና እረፍት አስፈላጊ ናቸው። '
            'ዘመናዊ ህክምና ብዙ በሽታዎችን ማከም ይችላል። '
            'ክትባት ተላላፊ በሽታዎችን ለመከላከል ወሳኝ ሚና ይጫወታል። '
            'ንጹህ ውሃ እና ንፅህና ጤናን ለመጠበቅ ይረዳሉ።'
        ),
    },

    # ── TIGRINYA ─────────────────────────────────────────────────────────
    {
        'title': 'ናይ ሓበሬታ ምድላይ',
        'language': 'tigrinya',
        'raw_text': (
            'ናይ ሓበሬታ ምድላይ ካብ ስብስብ ሰነዳት ዝምልከት ሓበሬታ ናይ ምርካብ ሂደት እዩ። '
            'ናይ ምድላይ ሞተራት ሰነዳት ንምምዳብን ንምድላይን ይጥቀሙ። '
            'ቬክተር ቦታ ሞዴልን BM25ን ዋና ዋና ኣገባባት እዮም። '
            'ኢንዴክሲንግ ቅልጡፍ ምድላይ ሰነዳት ይፈቅድ።'
        ),
    },
    {
        'title': 'ኤርትራን ኢትዮጵያን ታሪኽ',
        'language': 'tigrinya',
        'raw_text': (
            'ትግርኛ ኣብ ኤርትራን ኢትዮጵያን ዝዝረብ ቋንቋ እዩ። '
            'ኣስመራ ናይ ኤርትራ ርእሰ ከተማ ኮይና ብታሪኻዊ ህንጻታታ ትፍለጥ። '
            'ኣኽሱም ጥንታዊ ስልጣነ ዝነበሮ ቦታ እዩ። '
            'ትግርኛ ቋንቋ ናይ ጌዝ ፊደል ይጥቀም።'
        ),
    },
    {
        'title': 'ሳይንስን ቴክኖሎጅን',
        'language': 'tigrinya',
        'raw_text': (
            'ሰብ ሰርሖ ኣእምሮ ናይ ዘመናዊ ቴክኖሎጅ ቀንዲ ክፋል ኮይኑ ኣሎ። '
            'ማሽን ለርኒንግ ኮምፒዩተራት ካብ ዳታ ክመሃሩ ይፈቅደሎም። '
            'ዲጂታል ቴክኖሎጅ ትምህርቲ፣ ጥዕናን ንግድን ቀይሩ ኣሎ። '
            'ናይ ተፈጥሮ ቋንቋ ሂደት ኮምፒዩተራት ቋንቋ ክርድኡ ይሕግዞም።'
        ),
    },

    # ── AFAN OROMO ───────────────────────────────────────────────────────
    {
        'title': 'Barbaadaa Odeeffannoo',
        'language': 'afan_oromo',
        'raw_text': (
            'Barbaadaa odeeffannoo jechuun odeeffannoo barbaachisaa ta\'e '
            'galmee keessaa argachuu dha. '
            'Injinii barbaadaa galmeelee qindeessuuf fi barbaaduf ni fayyadama. '
            'Moodeela bakka vektora fi BM25 maloota gurguddoo dha. '
            'Indeeksiin barbaadaa ariifataa galmeelee ni hayyama.'
        ),
    },
    {
        'title': 'Itoophiyaa fi Seenaa Ishee',
        'language': 'afan_oromo',
        'raw_text': (
            'Itoophiyaan biyya Afrikaa Bahaa keessa argamtu yoo ta\'u, '
            'seenaa dheeraa qabdi. '
            'Afaan Oromoo afaan naannoo Oromiyaa fi afaan hedduu namoota '
            'Itoophiyaa keessa jiraataniin dubbatama. '
            'Finfinnee magaalaa guddoo Itoophiyaa ti. '
            'Buna Itoophiyaa keessatti argame.'
        ),
    },
    {
        'title': 'Teknolojii fi Saayinsii',
        'language': 'afan_oromo',
        'raw_text': (
            'Sammuu namtolchee teknolojii ammayyaa keessatti bakka guddaa qaba. '
            'Barnoota maashinii kompiyuutaroonni deetaa irraa akka barataniif ni hayyama. '
            'Teknolojii dijitaalaa barnootaa, fayyaa fi daldala jijjiireera. '
            'Afaan uumamaa hojjechuun kompiyuutaroonni afaan akka hubataniif ni gargaara.'
        ),
    },
]


class Command(BaseCommand):
    help = 'Add sample documents in Amharic, Tigrinya, and Afan Oromo'

    def handle(self, *args, **options):
        self.stdout.write('Adding local language documents...\n')
        created = 0

        for d in DOCS:
            obj, new = Document.objects.get_or_create(
                title=d['title'],
                defaults={
                    'raw_text': d['raw_text'],
                    'language': d['language'],
                    'pub_date': timezone.now(),
                }
            )
            status = 'Created' if new else 'Already exists'
            flag = {'amharic': '🇪🇹', 'tigrinya': '🇪🇷', 'afan_oromo': '🟢'}.get(d['language'], '📄')
            self.stdout.write(f"  {flag} [{status}] {d['title']}")
            if new:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✓  {created} new documents added.'
        ))
        self.stdout.write(self.style.WARNING(
            'Now run:  python manage.py index_docs  to rebuild the index.'
        ))
