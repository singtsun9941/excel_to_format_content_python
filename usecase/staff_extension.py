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

def get_schedule_from_row(group):
    """Return a list of cleaned schedule dicts for the given row or group.

    Mapping rules:
    - If columns named '1'..'31' exist on the row, map those headers to their values.
    - Drop entries where the value is NaN.
    """

    # Support both string headers '1'..'31' and integer headers 1..31
    numeric_headers = [str(i) for i in range(1, 32)]
    schedules = []
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

    if entry:
        schedules.append(entry)

    return schedules

def clean_group_data(group):
    """Clean the group DataFrame by dropping unnecessary columns and rows."""
    import pandas as _pd

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
    cols_to_keep = [c for c in clean_group.columns if (c is not None and not (_pd.isna(c)))]
    clean_group = clean_group.loc[:, cols_to_keep]

    # Drop columns where all elements are NaN
    clean_group = clean_group.dropna(axis=1, how='all')
    # Drop rows where all elements are NaN
    clean_group = clean_group.dropna(axis=0, how='all')
    return clean_group
