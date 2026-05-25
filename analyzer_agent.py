def generate_insight(df):
    
    if df.empty:
        return "No data found."

    text = []

    if len(df.columns) >= 2:

        first_col = df.columns[0]
        second_col = df.columns[1]

        try:

            max_value = df[second_col].max()

            top_item = df[df[second_col] == max_value][first_col].values[0]

            text.append(
                f"The highest value in {second_col} belongs to {top_item}"
            )

        except:
            pass

    text.append(
        f"The dataset contains {len(df)} rows."
    )

    return " ".join(text)