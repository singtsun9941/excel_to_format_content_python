def create_staffs(df):
    """Create Staff objects from a raw DataFrame.

    This function lazily imports `clean_data` from `usecase.df_extension` to avoid
    circular imports when modules re-export each other's symbols.
    """
    from usecase.df_extension import clean_data

    staffs = []
    # Import Staff lazily to keep imports local and avoid import-time issues
    from model.Staff import Staff


    grouped = df.groupby('staff_name')
    for name, group in grouped:

        staff_id = group['staff_id'].iloc[0] if 'staff_id' in group.columns else None
        tel = group['tel'].iloc[0] if 'tel' in group.columns else None
        schedule = get_schedule_from_row(group)

        if (name != None):
            staffs.append(Staff(name=name, staffNo=staff_id, tel=tel, schedule=schedule))

    return staffs


def _is_missing(v):
    """Return True if value is considered missing (None, NaN, empty string).

    This is a lightweight replacement for pandas.isna to avoid importing pandas
    in helper utilities. It handles float('nan'), numpy.nan (via v!=v), None,
    and empty/blank strings.
    """
    if v is None:
        return True
    # float NaN
    if isinstance(v, str) and v.strip() == '':
        return True
    return False

def get_schedule_from_row(group):
    """Return a list of cleaned schedule dicts for the given row or group.

    Mapping rules:
    - If columns named '1'..'31' exist on the row, map those headers to their values.
    - Drop entries where the value is NaN.
    """

    # Support both string headers '1'..'31' and integer headers 1..31
    numeric_headers = [str(i) for i in range(1, 32)]
    entry = {}

    clean_group = clean_group_data(group)
    # prefer string and int headers 1..31 on the cleaned group
    for header in range(1, 32):
        # try int header first, then string header
        value = None
        if header in clean_group.columns:
            vals = clean_group[header].values.tolist()
            if vals:
                value = vals[0]
        else:
            hstr = str(header)
            if hstr in clean_group.columns:
                vals = clean_group[hstr].values.tolist()
                if vals:
                    value = vals[0]

        if value is not None:
            entry[header] = value

    return entry

def clean_group_data(group):
    """Clean the group DataFrame by dropping unnecessary columns and rows."""
    # lightweight missing check used instead of pandas.isna
    # Work on a copy
    clean_group = group.copy()

    # Normalize/strip string column names and convert empty strings to None
    orig_cols = list(clean_group.columns)
    new_cols = []
    for c in orig_cols:
        if isinstance(c, str):
            nc = c.strip()
            if nc == "":
                nc = None
        else:
            nc = c
        new_cols.append(nc)

    clean_group.columns = new_cols

    # Build list of columns to keep (exclude None or NaN headers)
    cols_to_keep = [c for c in clean_group.columns if (c is not None and not _is_missing(c))]
    clean_group = clean_group.loc[:, cols_to_keep]

    # Drop columns where all elements are NaN
    clean_group = clean_group.dropna(axis=1, how='all')
    # Drop rows where all elements are NaN
    clean_group = clean_group.dropna(axis=0, how='all')
    return clean_group

def get_schedule_list(staffs):
    """Return a list of all staff schedules."""
    schedules = []
    for staff in staffs:
        for k, v in staff.schedule.items():
            if not _is_missing(v):
                if not v in schedules:
                    schedules.append(v)
    return schedules