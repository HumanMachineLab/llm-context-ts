from cached_property import cached_property
import sqlite3
from sqlite3 import Error
from typing import List, Tuple, Protocol
import math
import os
import numpy as np

# change the execution path to filepath for relative db file import
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


TRAIN_TEST_SPLIT = 0.75


class DB:
    def __init__(self, dataset_type, table_type=""):
        self.dataset_type = dataset_type
        self.table_type = table_type
        if dataset_type in ["city", "disease"]:
            self.table_name = "wikisection_" + dataset_type
        elif dataset_type in ["academic", "product", "committee"]:
            self.table_name = "qmsum_" + dataset_type
        else:
            self.table_name = dataset_type

        if table_type == "augmented":
            self.table_name += "_gpt_augmented"
        elif table_type == "train_test":
            self.table_name += "_train_test"
        elif table_type == "test":
            self.table_name += "_test"
        elif table_type == "validation":
            self.table_name += "_validation"
        elif table_type == "gta1":
            self.table_name += "_gta1"
        elif table_type == "gta2":
            self.table_name += "_gta2"

        self.db_file = os.path.join(dname, f"{dataset_type}.db")

        self.migrate_table()

    @cached_property
    def conn(self):
        """create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e, self.db_file)

        return conn

    def create_table(self, create_table_sql):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def get_num_rows(self):
        sql = f"""SELECT COUNT(*) FROM {self.table_name}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]

    def get_num_segments(self):
        sql = f"""SELECT COUNT(*) FROM {self.table_name} WHERE target=?"""
        cur = self.conn.cursor()
        cur.execute(sql, (1,))
        return cur.fetchone()[0]

    def create_sentence(self, sentence):
        sql = f""" INSERT INTO {self.table_name}(sentence,target,parent,sequence)
                VALUES(?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, sentence)
        self.conn.commit()
        return cur.lastrowid

    def create_segment(self, segment: List[str]):
        sql = f""" INSERT INTO {self.table_name}(sentence,target,parent,sequence)
                VALUES(?,?,?,?) """

        if len(segment) > 0:
            target_sentence_id = None
            cur = self.conn.cursor()
            # insert the target segment
            cur.execute(sql, (segment[0], 1, None, 0))
            self.conn.commit()
            target_sentence_id = cur.lastrowid

        if len(segment) > 1:
            remaining_segment = []
            for i, sentence in enumerate(segment[1:]):
                remaining_segment.append((sentence, 0, target_sentence_id, i + 1))

            cur.executemany(sql, remaining_segment)
            self.conn.commit()

        return target_sentence_id

    def insert_train_test_record(self, segment_id, type):
        sql = f""" INSERT INTO {self.table_name}_train_test(segment_id,type)
                VALUES(?,?) """

        cur = self.conn.cursor()
        # insert the target segment
        cur.execute(sql, (segment_id, type))
        self.conn.commit()
        target_sentence_id = cur.lastrowid

        return target_sentence_id

    def get_segment(self, segment_id, max_segment_size=1000):
        sql = f""" SELECT * FROM {self.table_name}
                WHERE id=? OR parent=? ORDER BY sequence ASC LIMIT ?"""

        cur = self.conn.cursor()
        cur.execute(sql, (segment_id, segment_id, max_segment_size))

        rows = cur.fetchall()

        return rows

    def get_target_sentences(self):
        sql = f""" SELECT * FROM {self.table_name}
                WHERE target=?"""

        cur = self.conn.cursor()
        cur.execute(sql, (1,))

        rows = cur.fetchall()

        return rows

    def get_target_sentence_ids(self, split="test"):
        train_test_table_name = "wikisection_" + self.dataset_type + "_train_test"
        sql = (
            f"""SELECT * FROM {train_test_table_name} WHERE type=? ORDER BY RANDOM()"""
        )

        cur = self.conn.cursor()
        cur.execute(sql, (split,))

        rows = cur.fetchall()

        return rows

    def get_random_target_sentences(self, num_sentences, split="test"):
        target_sentence_ids = self.get_target_sentence_ids(split)[:num_sentences]
        sql = f"""SELECT * FROM {self.table_name} WHERE id=?"""

        rows = []
        for i in target_sentence_ids:
            # the id of the segment is the second column
            target_sentence_id = i[1]
            cur = self.conn.cursor()
            cur.execute(sql, (target_sentence_id,))

            row = cur.fetchall()
            rows.append(*row)

        return rows

    def get_random_segments(
        self,
        num_segments,
        split="test",
        max_segment_size=1000,
        artificial_segments=False,
    ):
        target_sentences = self.get_random_target_sentences(num_segments, split)
        segments = []
        for sentence in target_sentences:
            if not artificial_segments:
                segments.append(self.get_segment(sentence[0], max_segment_size))
            elif artificial_segments:
                # most segments don't exceed 1000 sentences anyways
                curr_segment = self.get_segment(sentence[0], 1000)
                artificial_segment = []
                for i, sentence in enumerate(curr_segment):
                    if len(artificial_segment) == 0:
                        # force the first label in the artificial segment to be 1
                        # has to be converted to tuple first.
                        sentence = list(sentence)
                        sentence[2] = 1
                        sentence = tuple(sentence)
                    artificial_segment.append(sentence)
                    if (i + 1) % max_segment_size == 0 or (i + 1) % len(
                        curr_segment
                    ) == 0:
                        # append the accumulated segment and dump
                        segments.append(artificial_segment)
                        artificial_segment = []

        return segments

    def get_random_segments_pct(
        self, pct_data=1, split="test", max_segment_size=1000, artificial_segments=False
    ):
        num_segments = self.get_num_segments()
        num_segments_to_fetch = math.floor(num_segments * pct_data)
        return self.get_random_segments(
            num_segments=num_segments_to_fetch,
            split=split,
            max_segment_size=max_segment_size,
            artificial_segments=artificial_segments,
        )

    def get_all(self):
        sql = f"""SELECT * FROM {self.table_name} ORDER BY id ASC"""

        cur = self.conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()

        return rows

    def get_all_segments(self):
        sentences = self.get_all()
        segments = []

        new_segment = []
        for sentence in sentences:
            if sentence[2] == 1:
                if len(new_segment) > 0:
                    segments.append(new_segment)
                    new_segment = []
                new_segment.append(sentence)
            else:
                new_segment.append(sentence)
        return segments


class Table(DB):
    def migrate_table(self):
        print("Using dataset: " + self.table_name)
        sql_create_table = f""" CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id integer PRIMARY KEY,
                                sentence text NOT NULL,
                                target integer NOT NULL,
                                parent integer,
                                sequence integer NOT NULL
                            ); """

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_table)


class AugmentedTable(DB):
    def __init__(self, dataset_type, table_type=""):
        super().__init__(dataset_type, "augmented")

    def migrate_table(self):
        sql_create_augmented_table = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                                            id integer PRIMARY KEY,
                                            augmented_sentence text NOT NULL,
                                            target integer NOT NULL,
                                            {self.dataset_type}_id integer NOT NULL,
                                            sequence integer NOT NULL,
                                            FOREIGN KEY ({self.dataset_type}_id) REFERENCES {self.dataset_type} (id)
                                        );"""

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_augmented_table)

    def create_augmented_sentence(self, augmented_sentence):
        sql = f""" INSERT INTO {self.table_name}(augmented_sentence,target,sequence,{self.dataset_type}_id)
                VALUES(?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, augmented_sentence)
        self.conn.commit()
        return cur.lastrowid

    def get_augmented_sentences(self, real_sentence_id: int):
        sql = f"""SELECT * FROM {self.table_name} WHERE {self.dataset_type}_id=? ORDER BY """

        cur = self.conn.cursor()
        cur.execute(sql, (1, real_sentence_id))

        rows = cur.fetchall()

        return rows


class GTA1Table(DB):
    def __init__(self, dataset_type, table_type=""):
        super().__init__(dataset_type, "gta1")

    def migrate_table(self):
        sql_create_gta1_table = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                                            id integer PRIMARY KEY,
                                            augmented_sentence text NOT NULL,
                                            target integer NOT NULL,
                                            {self.dataset_type}_id integer NOT NULL,
                                            sequence integer NOT NULL,
                                            FOREIGN KEY ({self.dataset_type}_id) REFERENCES {self.dataset_type} (id)
                                        );"""

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_gta1_table)

    def create_augmented_sentence(self, augmented_sentence):
        sql = f""" INSERT INTO {self.table_name}(augmented_sentence,target,sequence,{self.dataset_type}_id)
                VALUES(?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, augmented_sentence)
        self.conn.commit()
        return cur.lastrowid

    def get_augmented_sentences(self, real_sentence_id: int):
        sql = f"""SELECT * FROM {self.table_name} WHERE {self.dataset_type}_id=? ORDER BY """

        cur = self.conn.cursor()
        cur.execute(sql, (1, real_sentence_id))

        rows = cur.fetchall()

        return rows


class GTA2Table(DB):
    def __init__(self, dataset_type, table_type=""):
        super().__init__(dataset_type, "gta2")

    def migrate_table(self):
        sql_create_gta2_table = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                                            id integer PRIMARY KEY,
                                            augmented_sentence text NOT NULL,
                                            target integer NOT NULL,
                                            {self.dataset_type}_id integer NOT NULL,
                                            sequence integer NOT NULL,
                                            FOREIGN KEY ({self.dataset_type}_id) REFERENCES {self.dataset_type} (id)
                                        );"""

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_gta2_table)

    def create_augmented_sentence(self, augmented_sentence):
        sql = f""" INSERT INTO {self.table_name}(augmented_sentence,target,sequence,{self.dataset_type}_id)
                VALUES(?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, augmented_sentence)
        self.conn.commit()
        return cur.lastrowid

    def get_augmented_sentences(self, real_sentence_id: int):
        sql = f"""SELECT * FROM {self.table_name} WHERE {self.dataset_type}_id=? ORDER BY """

        cur = self.conn.cursor()
        cur.execute(sql, (1, real_sentence_id))

        rows = cur.fetchall()

        return rows


class TestTable(DB):
    def __init__(self, dataset_type, table_type=""):
        super().__init__(dataset_type, "test")

    def migrate_table(self):
        sql_create_test_table = f""" CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id integer PRIMARY KEY,
                                sentence text NOT NULL,
                                target integer NOT NULL,
                                parent integer,
                                sequence integer NOT NULL
                            ); """

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_test_table)


class ValidationTable(DB):
    def __init__(self, dataset_type, table_type=""):
        super().__init__(dataset_type, "validation")

    def migrate_table(self):
        sql_create_validation_table = f""" CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id integer PRIMARY KEY,
                                sentence text NOT NULL,
                                target integer NOT NULL,
                                parent integer,
                                sequence integer NOT NULL
                            ); """

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_validation_table)


class TrainTestTable(DB):
    def __init__(self, dataset_type):
        super().__init__(dataset_type, "train_test")
        self.dataset_type = dataset_type

    def migrate_table(self):
        sql_create_train_test_table = f""" CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id integer PRIMARY KEY,
                                segment_id integer NOT NULL,
                                type text NOT NULL,
                                FOREIGN KEY (segment_id) REFERENCES {self.dataset_type} (id)
                            ); """

        # create tables
        if self.conn is not None:
            self.create_table(sql_create_train_test_table)

    def create_train_test_split(self) -> None:
        sql_delete = f"""DELETE from {self.table_name}"""

        cur = self.conn.cursor()
        cur.execute(sql_delete)

        table = Table(self.dataset_type)

        target_sentences = table.get_target_sentences()
        ids = [s[0] for s in target_sentences]

        split = int(TRAIN_TEST_SPLIT * len(ids))

        np.random.shuffle(ids)
        train = [(x, "train") for x in ids[:split]]
        test = [(x, "test") for x in ids[split:]]

        sql = f""" INSERT INTO {self.table_name}(segment_id,type)
                VALUES(?,?) """

        cur.executemany(sql, train)
        cur.executemany(sql, test)
        self.conn.commit()
