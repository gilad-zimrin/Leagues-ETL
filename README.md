<div dir="rtl">

# תכנון

## תיאור המשימה
במשימה נדרש לתכנן וליצור ETL pipline על מנת לעכל, לסכם, לשמור ולהנגיש מידע על קבוצות בPremier League.

כרגע ניקח את המידע משני מקורות מידע:
https://api-sports.io/
https://apifootball.com/
למרות שכמובן שבמשימה נרצה לאפשר להוסיף מקורות מידע נוספים בקלות.

המידע שנשתמש בו (על פי הדרישה) זה המידע שהראוטים מנגישים על teams ו-standings.

נאפשר הנגשה של המידע החוצה ללקוחות בעזרת RestAPI בעזרת הספרייה FastAPI.

### מטרות חשובות שנרצה לשים לב בביצוע המשימה:

- נרצה לאפשר הוספה של מקורות מידע/שינויים בקלות, מבלי לפגוע/לשנות גרסאות קיימות.
- נרצה לאפשר לעלות את ה-scale  בכמה שפחות עבודה.
- נרצה לבנות בצורה יעילה מבחינת מהירות, משאבים, מחיר וכו..
- נרצה לטפל ביעילות בשגיאות, ולתעד אותן
- נרצה לאפשר הרצה אסינכרונית כל X זמן, כך שגם עבור X קטן מאוד שני Instances או יותר ירוצו במקביל בלי בעיה.
- ניצור שרת mock שידמה את השרתים החיצוניים, על מנת לא להיות תלויים בהם בבדיקות שלנו ובכדי לא להעמיס עליהם (במידה שהם עובדים לא טוב/אנחנו נרצה להריץ בדיקות עומסים)


## כלים וטכנולוגיות
נבצע את המשימה בעזרת שירות microservice בpython:

- התהליך יחסית פשוט, לכן נרצה שיתאפשר לנו לשלוט בהכל במקום אחד.
- נעבוד בצורת OOP על מנת לאפשר להתמודד בקלות ובמהירות עם  שינויים בסכמה, במידע שחוזר מהשרתים החיצוניים, או עם הוספה של שרתים נוספים.
- יהיה לנו מרחב פעולה עם ניטור וטיפול בשגיאות - נוכל להוציא שגיאות/לוגים/מידע מדוייק על החלקים הרלוונטיים בpipline, נדע מה בדיוק מה קרה בכל שלב. 
- נבנה את הרכיב בצורה אסינכרונית על מנת שהוא יהיה מסוגל להתמודד עם עומסים גדולים ו-scaling יהיה קל ופשוט.
- נחסוך כסף - לא נצטרך להשתמש בשרתים חצוניים בתשלום, כל מה שנצטרך זה לנהל פוד אחד בענן.

## ספריות פייתון מרכזיות

- apshceduler: על מנת שנהיה מסוגלים לתזמן משימות כל X זמן. בנוסף הספרייה מאפשר לנו להריץ במקביל מספר איטרציות (במקרה שהcron שלנו קטן יותר מהזמן שלוקח להריץ את תהליך הETL)
- fastapi: הספרייה הכי טובה ליצירת שרתים, מאפשרת ליצור שרת מהיר ואסינכרוני בקלות.
- google-cloud-bigquery: הספרייה הפייתונית על מנת להשתמש בbigquery.
- pydantic: ספרייה שמאפשר לנו להגדיר types של אובייקטים, ולבצע להם ולידציה פשוטה או מסובכת לפי הצרכים שלנו


## תכנון המימוש

קודם כל, נחליט על סכמה של המידע שנעביר, לאחר מכן, 
נרשום את השלד של התכנון של המימוש של הרכיב שלנו, על מנת להמחיש את הflow המרכזי בקוד.

### מבנה הסכמה:

את המבנה המדוייק של הסכמה ניתן לראות בקובץ team_info_schema אבל זה ארוך ופחות מובן,
לכן נרשום פה את ה-pydantic type שהוא יותר ברור.

#### קבלת החלטות באפיון הסכמה, והנחות שהנחתי:

על מנת להחליט איך להגדיר את הסכמה עקבתי על פי ההוראות, 10-15 שדות, חלקם מהאובייקט "teams" - (team name, foundation year,
home stadium, city) וחלקם מהאובייקט “standings" - (table position, wins,
losses, goals scored).

את הטייפים שחזרו בint שמרתי בתור int, ואת הטייפים שחזרו בתור string (והם לא מספר שאפשר להפוף לint) שמרתי בתור string.

הנחתי מספר הנחות, בעיקר בהתבסס על הכמות הקטנה של מידע שאני דגמתי:

 - הטייפים של השדות לא משתנים (שדה שחזר לי ב3 בקשות שונות באותו ראוט בתור int, אני מניח שהוא יחזור בתור int גם עבור פרמטרים שונים באותה בקשה).
 - שדות שקיימים בכמה בקשות עם הפרמטרים שאני ביצעתי יהיו קיימים גם בבקשות דומות אחרות, ולפי ההנחה הזאת הגדרתי אותם כ"חובה" בסכמה.


</div>

```python
class TeamInfo(BaseModel):
    id: StrictInt
    name: StrictStr
    country: StrictStr
    founded: Optional[StrictInt]
    venue_name: Optional[StrictStr]
    venue_address: Optional[StrictStr]
    venue_city: Optional[StrictStr]
    venue_capacity: Optional[StrictInt]
    venue_surface: Optional[StrictStr]
    league_id: Optional[StrictInt]
    league_name: Optional[StrictStr]
    league_country: Optional[StrictStr]
    rank: Optional[StrictInt]
    points: Optional[StrictInt]
    overall_wins: Optional[StrictInt]
    overall_draws: Optional[StrictInt]
    overall_loses: Optional[StrictInt]
    overall_goals_for: Optional[StrictInt]
    overall_goals_against: Optional[StrictInt]
```
```sql
CREATE TABLE `footballleagues.team_info.team_info` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    country STRING NOT NULL,
    founded INT64,
    venue_name STRING,
    venue_address STRING,
    venue_city STRING,
    venue_capacity INT64,
    venue_surface STRING,
    league_id INT64 NOT NULL,
    league_name STRING NOT NULL,
    league_country STRING NOT NULL,
    rank INT64 NOT NULL,
    points INT64 NOT NULL,
    overall_wins INT64 NOT NULL,
    overall_draws INT64 NOT NULL,
    overall_loses INT64 NOT NULL,
    overall_goals_for INT64 NOT NULL,
    overall_goals_against INT64 NOT NULL
);

```
<div dir="rtl">

### מבנה הקוד:

בקובץ ה-main נרשום את הscheduler שיתזמן את הקריאה להתחלת ה-ETL ואת הקריאה להפעלה של ה-app.
במערך שלמעלה יש את כל הETL-ים עבור כל מקור מידע, ואת האינטרוול שהם ירוצו איתו (אפשר להפוך את זה למשתנים נפרדין במידת הצורך).

</div>

```python
all_data_sources_etls = [
    (FootballApiETL(), scheduler_interval_minutes * 60),
    (APIFootballETL(), scheduler_interval_minutes * 60)
]

def run_fast_api_app():
    pass



async def run_scheduler():
    scheduler = AsyncIOScheduler()
    for source_etl in all_data_sources_etls:
        scheduler.add_job(
            source_etl[0].execute,
            'interval',
            seconds=source_etl[1],
            next_run_time=datetime.now(),
        )
    scheduler.start()
    Thread(target=run_fast_api_app).start()

    try:
        await Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

```
<div dir="rtl">

לאחר מכן נגדיר את המחלקות שלנו:

### על מנת לאפשר חלוקה נכונה של התפקידים, ולשמור על עקרונות הSOLID, נבנה שתי מחלקות בסיס עיקריות:

#### מחלקת BaseETL:

מטרת המחלקה היא להגדיר תהליך ETL גנרי עבור כל מקורות המידע שנשתמש בהם.
כל מקור מידע יצור מחלקה שיורשת ממחלקת הבסיס הזאת, כך שהוא ישתמש בפונקציות load ו-execute של מחלקת הבסיס, ויממש בעצמו פונקציות extract ו-transform.

לכל תהליך ETL יהיה etl_instance_id שיופיע בלוגים וישמש אותנו לעקוב אחר תהליך שלם.

המחלקה הזאת תשמור על סטנדרט אחיד לכל מקורות המידע, ותדריך אותנו איזה פונקציות צריך ליצור עבור כל מקור מידע, כל שהוספה של מקורות מידע נוספים תהיה פשוטה.


</div>

```python
class BaseETL(ABC):
    def __init__(self):
        self.etl_instance_id = uuid4()
        self.bigquery_handler: BigQueryHandler = BigQueryHandler()

    @property
    @abstractmethod
    def api_host(self):
        pass

    @property
    @abstractmethod
    def current_league_id(self):
        pass

    @abstractmethod
    async def extract(self) -> Dict | List:
        pass

    @abstractmethod
    def transform(self, raw_data):
        pass


    def load(self, rows: List[Dict], table_name: str = team_info_table):
        """
        Batch load a list of validated dicts into BigQuery.
        """
        if not rows:
            return True

        try:
            self.bigquery_handler.insert_batch(table_name, rows)
        except Exception as err:
            logger.exception("An unexpected error has occurred on load function")
            raise RuntimeError(f"Failed to load data into BigQuery: {err}") from err


    async def save_raw_data(self, raw_data):
        """
        Saving raw data to BigQuery or non-rational database for monitoring, if needed
        :return:
        """
        pass


    async def execute(self):
        try:
            logger.info("Started a new ETL instance", extra={
                'etl_instance_id': self.etl_instance_id
            })
    
            raw_data = await self.extract()
            logger.debug("Successfully extracted data", extra={
                'etl_instance_id': self.etl_instance_id
            })
    
            asyncio.create_task(self.save_raw_data(raw_data))
    
    
            processed_objects = self.transform(raw_data)
            logger.debug(f"Successfully transformed {processed_objects} rows into TeamInfo dict", extra={
                'etl_instance_id': self.etl_instance_id
            })
    
            self.load(processed_objects)
    
            logger.debug(f"Successfully loaded {processed_objects} rows into team_info table", extra={
                'etl_instance_id': self.etl_instance_id
            })
    
            logger.info("Successfully finished ETL process", extra={
                'etl_instance_id': self.etl_instance_id
            })
        except (Exception,):
            logger.exception("An unexpected error has occurred in execute", extra={
                'etl_instance_id': self.etl_instance_id
            })


```
<div dir="rtl">

#### מחלקת SourceETL

מחלקה שתירש ממחלקת הבסיס BaseETL ותממש את הפונקציות הייחודיות למקור המידע הספציפי הזה.

תפקיד המחלקה זה להתאים את הETL הגנרי שלנו לכל מקור מידע ספציפי, זה מאפשר לנו להוסיף מקורות מידע חדשים מבלי לשנות את המקורות המידע הישנים, על מנת לא לפגוע בקוד "פרודי" שכבר נבדק ועובד.

לדוגמא, עבור מקור המידע FootballAPI ניצור את:


</div>

```python
class FootballApiETL(BaseETL):
    def __init__(self):
        super().__init__()
        self.current_season = getenv("FOOTBALL_API_CURRENT_SEASON")

        self.teams_url = f"{self.api_host}teams?league={self.current_league_id}&season={self.current_season}"
        self.standings_url = \
            f"{self.api_host}standings?league={self.current_league_id}&season={self.current_season}&team="
        self.headers = {
            'x-apisports-key': getenv("X_APISPORTS_KEY")
        }

    @property
    def api_host(self):
        return getenv("FOOTBALL_API_SPORTS_HOST")

    @property
    def current_league_id(self):
        return getenv("FOOTBALL_API_CURRENT_LEAGUE")


    async def extract(self) -> Dict | List:
        pass


    def transform(self, raw_object) -> TeamInfo:
        pass


```
<div dir="rtl">

#### מחלקת BigQueryHandler

מחלקת עזר, שתפקידה לנהל את כלח הפעולות מול הBigQuery, על מנת לחלק סמכויות מה-ETL בצורה יותר נכונה והגיונית.

</div>

```python
class BigQueryHandler:
    """
    BigQuery helper for:
    - Batch inserts with load_table_from_json
    - Query helpers (get_one, get_by_params, get_all)
    """

    def __init__(self):
        self.project_id = project_id
        self.client = bigquery.Client()

    def insert_batch(self, table_name: str, rows: list[dict]):
        pass

    def get_all(self, table_name: str):
        pass


```
<div dir="rtl">

#### היתרונות בלעבוד עם BigQuery:

- המידע נשמר לפי עמודות, אם יש לנו מאות שדות ואנחנו מבקשים רק 5, בקשות על כמויות עצומות של מידע יפעלו מאוד במהירות.
- שרת חיצוני - התחזוקה והניהול שלו לא באחריותנו.
- יחסית זול, בניגוד למתחרים כגון snowflake ו-redshift.
- בנוי עם מקביליות - מספר גדול של לקוחות יכולים לגשת בו זמנית באין מפריע
- מתאים לשרת שלנו, שרת שמכניס בקשות בbatch ומאפשר קריאה של כמויות עצומות של מידע בבת אחת


</div>
