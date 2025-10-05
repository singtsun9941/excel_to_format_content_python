def create_staffs(df):
    """Create Staff objects from a raw DataFrame.

    This function lazily imports `clean_data` from `usecase.df_extension` to avoid
    circular imports when modules re-export each other's symbols.
    """
    from usecase.df_extension import clean_data

    new_df = clean_data(df)

    staffs = []
    # Import Staff lazily to keep imports local and avoid import-time issues
    from model.Staff import Staff

    if 'staff_id' in new_df.columns:
        grouped = new_df.groupby('staff_id')
        for staff_id, group in grouped:
            name = group['staff_name'].iloc[0] if 'staff_name' in group.columns else None
            # If a 'tel' column exists, take the first non-null value as the staff telephone
            tel = None
            if 'tel' in group.columns:
                non_null_tels = group['tel'].dropna().tolist()
                if non_null_tels:
                    tel = non_null_tels[0]
            schedule = []
            for _, row in group.iterrows():
                row_dict = row.to_dict()
                row_dict.pop('staff_name', None)
                row_dict.pop('staff_id', None)
                # remove tel from schedule entries since it's an attribute of Staff
                row_dict.pop('tel', None)
                schedule.append(row_dict)

            staffs.append(Staff(name=name, staffNo=staff_id, tel=tel, schedule=schedule))
    else:
        for _, row in new_df.iterrows():
            row_dict = row.to_dict()
            name = row_dict.pop('staff_name', None)
            staff_id = row_dict.pop('staff_id', None)
            # Extract tel if present on the row
            tel = row_dict.pop('tel', None)
            schedule = [row_dict]
            staffs.append(Staff(name=name, staffNo=staff_id, tel=tel, schedule=schedule))

    return staffs
