import pytest
from file_parser.file_parser import check_file, check_tags


def test_valid_file():
    content = """\
[Event "Example Game"]
[Site "N/A"]
[Date "2005-01-20"]
[Round "-"]
[X "DummyX"]
[O "DummyO"]
[Result "0-1"]
[Termination "DummyO wins by tic-tac-toe"]

1. E3 E7 2. D1 B1 3. E1 D2 4. A5 A6 5. C9 H7 6. F1 I2 7. H5 E6 8. D8 B4 
9. H2 E4 10. G6 C7 11. I1 H3 12. E9 D7 13. B2 F4 14. H1 G4 15. A3 A8 16. C4 G2 
17. C5 H6 18. D9 B8 19. F5 H4 20. E8 D5 21. A4 B3 22. F8 I5 23. G5 B6 24. A1 A2 
25. C6 I9 26. H9 I4 27. G1 C3 28. I8 C2 29. A7 C1 30. B7 G9 31. A9 C8 32. D6 E5 
33. G7 G8 34. H8 I7 0-1
"""
    assert check_file(content) is True


def test_missing_tag():
    content = """\
[Event "Missing Result Game"]
[Site "N/A"]
[Date "2005-01-20"]
[Round "-"]
[X "DummyX"]
[O "DummyO"]

1. E3 E7 2. D1 B1 3. E1 D2 4. A5 A6 5. C9 H7 6. F1 I2 7. H5 E6 8. D8 B4 
9. H2 E4 10. G6 C7 11. I1 H3 12. E9 D7 13. B2 F4 14. H1 G4 15. A3 A8 16. C4 G2 
17. C5 H6 18. D9 B8 19. F5 H4 20. E8 D5 21. A4 B3 22. F8 I5 23. G5 B6 24. A1 A2 
25. C6 I9 26. H9 I4 27. G1 C3 28. I8 C2 29. A7 C1 30. B7 G9 31. A9 C8 32. D6 E5 
33. G7 G8 34. H8 I7 0-1
"""
    assert check_file(content) is False


def text_invalid_result():
    content = """\
    [Event "Example Game"]
    [Site "N/A"]
    [Date "2005-01-20"]
    [Round "-"]
    [X "DummyX"]
    [O "DummyO"]
    [Result "invalidresult"]
    [Termination "DummyO wins by tic-tac-toe"]

    1. E3 E7 2. D1 B1 3. E1 D2 4. A5 A6 5. C9 H7 6. F1 I2 7. H5 E6 8. D8 B4 
    9. H2 E4 10. G6 C7 11. I1 H3 12. E9 D7 13. B2 F4 14. H1 G4 15. A3 A8 16. C4 G2 
    17. C5 H6 18. D9 B8 19. F5 H4 20. E8 D5 21. A4 B3 22. F8 I5 23. G5 B6 24. A1 A2 
    25. C6 I9 26. H9 I4 27. G1 C3 28. I8 C2 29. A7 C1 30. B7 G9 31. A9 C8 32. D6 E5 
    33. G7 G8 34. H8 I7 0-1
    """
    assert check_file(content) is False


def test_invalid_move_format():
    content = """\
[Event "Invalid Move Format Game"]
[Site "N/A"]
[Date "2024-12-18"]
[Round "-"]
[X "DummyX"]
[O "Dummy)"]
[Result "1/2-1/2"]

1. E3 E7 2. D1 Z10 3. E1 D2
"""
    assert check_file(content) is False


def test_repeat_move():
    content = """\
[Event "Repeated Move Game"]
[Site "N/A"]
[Date "2024-12-18"]
[Round "-"]
[X "RandoTron"]
[O "RandoTron"]
[Result "1/2-1/2"]

1. E3 E3 2. D1 B1 3. E1 D2
"""
    assert check_file(content, strict=True) is False

def test_invalid_move_order():
    content = """\
    [Event "Invalid Move Order Game (2. D2 before 2. B1)"]
    [Site "N/A"]
    [Date "2005-01-20"]
    [Round "-"]
    [X "DummyX"]
    [O "DummyO"]
    [Result "0-1"]
    [Termination "DummyO wins by tic-tac-toe"]

    1. E3 E7 2. D2 B1 3. E1 D2 4. A5 A6 5. C9 H7 6. F1 I2 7. H5 E6 8. D8 B4 
    9. H2 E4 10. G6 C7 11. I1 H3 12. E9 D7 13. B2 F4 14. H1 G4 15. A3 A8 16. C4 G2 
    17. C5 H6 18. D9 B8 19. F5 H4 20. E8 D5 21. A4 B3 22. F8 I5 23. G5 B6 24. A1 A2 
    25. C6 I9 26. H9 I4 27. G1 C3 28. I8 C2 29. A7 C1 30. B7 G9 31. A9 C8 32. D6 E5 
    33. G7 G8 34. H8 I7 0-1
    """
    assert check_file(content, strict=True) is False


def test_extra_tag():
    content = """\
    [Event "Example Game"]
    [Site "N/A"]
    [Date "2005-01-20"]
    [Round "-"]
    [X "DummyX"]
    [O "DummyO"]
    [Result "0-1"]
    [Termination "DummyO wins by tic-tac-toe"]
    [ExtraTag "ExtraValue"]

    1. E3 E7 2. D1 B1 3. E1 D2 4. A5 A6 5. C9 H7 6. F1 I2 7. H5 E6 8. D8 B4 
    9. H2 E4 10. G6 C7 11. I1 H3 12. E9 D7 13. B2 F4 14. H1 G4 15. A3 A8 16. C4 G2 
    17. C5 H6 18. D9 B8 19. F5 H4 20. E8 D5 21. A4 B3 22. F8 I5 23. G5 B6 24. A1 A2 
    25. C6 I9 26. H9 I4 27. G1 C3 28. I8 C2 29. A7 C1 30. B7 G9 31. A9 C8 32. D6 E5 
    33. G7 G8 34. H8 I7 0-1
    """
    assert check_tags(content, strict=False) is True
    assert check_tags(content, strict=True) is False


def test_missing_moves():
    content = """\
[Event "Bot Game"]
[Site "N/A"]
[Date "2024-12-18"]
[Round "-"]
[X "RandoTron"]
[O "RandoTron"]
[Result "1/2-1/2"]
"""
    assert check_file(content) is False
