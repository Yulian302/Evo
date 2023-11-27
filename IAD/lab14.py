import atoti as tt

session = tt.session.Session(name="Sales Booster")

holidays_events = session.read_csv(
    "data/holidays_events.csv",
    keys=["date", "locale_name"],
)
print(holidays_events.head())
cube = session.create_cube(holidays_events, name='Holidays events')
