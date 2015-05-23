from initialize_registry import load_registry
import registry as r


def run():
    # grant all privileges on *.* to trivia_challenge@localhost identified by '9a7123w4982ew3490x23pl34bz' with grant option; # NOQA
    load_registry()
    r.get_registry()['MY_SQL'].query(
        """CREATE TABLE questions(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            prompt VARCHAR(255),
            passing_score INT,
            correct_names LONGTEXT,
            finalized INT DEFAULT 1,
            active INT DEFAULT 1,
            total INT DEFAULT 0
        )"""
    )

if __name__ == "__main__":
    run()
