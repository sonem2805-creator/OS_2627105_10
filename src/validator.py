import pandas as pd


class Validator:

    REQUIRED_COLUMNS = [
        "Process",
        "Allocation_A",
        "Allocation_B",
        "Allocation_C"
    ]

    @staticmethod
    def validate(df):

        Validator.check_empty(df)

        Validator.check_columns(df)

        Validator.check_available_row(df)

        Validator.check_numeric(df)

        Validator.check_negative(df)

        Validator.check_allocation_max(df)

        return True

    @staticmethod
    def check_empty(df):

        if df.empty:
            raise ValueError(
                "CSV file is empty."
            )

    @staticmethod
    def check_columns(df):

        for column in Validator.REQUIRED_COLUMNS:

            if column not in df.columns:

                raise ValueError(
                    f"Missing required column: {column}"
                )

    @staticmethod
    def check_available_row(df):

        available_rows = df[
            df["Process"].astype(str).str.upper()
            == "AVAILABLE"
        ]

        if available_rows.empty:

            raise ValueError(
                "AVAILABLE row is missing."
            )

    @staticmethod
    def check_numeric(df):

        process_rows = df[
            df["Process"].astype(str).str.upper()
            != "AVAILABLE"
        ]

        numeric_columns = []

        for column in df.columns:

            if column != "Process":

                numeric_columns.append(column)

        for column in numeric_columns:

            for value in process_rows[column]:

                try:

                    if pd.isna(value):

                        raise ValueError()

                    float(value)

                except:

                    raise ValueError(
                        f"Invalid value in {column}: {value}"
                    )

    @staticmethod
    def check_negative(df):

        process_rows = df[
            df["Process"].astype(str).str.upper()
            != "AVAILABLE"
        ]

        numeric_columns = []

        for column in process_rows.columns:

            if column != "Process":

                numeric_columns.append(column)

        for column in numeric_columns:

            values = pd.to_numeric(
                process_rows[column]
            )

            if (values < 0).any():

                raise ValueError(
                    f"Negative value detected in {column}"
                )

    @staticmethod
    def check_allocation_max(df):

        max_columns_exist = (
            "Max_A" in df.columns
            and "Max_B" in df.columns
            and "Max_C" in df.columns
        )

        if not max_columns_exist:

            return

        process_rows = df[
            df["Process"].astype(str).str.upper()
            != "AVAILABLE"
        ]

        resources = ["A", "B", "C"]

        for resource in resources:

            allocation = pd.to_numeric(
                process_rows[f"Allocation_{resource}"]
            )

            maximum = pd.to_numeric(
                process_rows[f"Max_{resource}"]
            )

            if (allocation > maximum).any():

                raise ValueError(
                    f"Allocation_{resource} exceeds Max_{resource}"
                )
