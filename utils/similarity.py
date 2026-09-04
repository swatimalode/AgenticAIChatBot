import math


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)

"""
    The cosine_similarity() function calculates how similar two vectors are by measuring the 
    angle between them. In an AI application, these vectors can represent embeddings of text. 
    The function takes two vectors, a and b, as input.

    For example:

        a = [1, 2]
        b = [3, 4]

    First, the function calculates the dot product:

        dot_product = sum(x * y for x, y in zip(a, b))

    zip(a, b) pairs the values from both vectors:

        (1, 3)
        (2, 4)

    Then it multiplies each pair:

        1 * 3 = 3
        2 * 4 = 8

    Then sum() adds the results:

        3 + 8 = 11

    Therefore:

        dot_product = 11

    Next, the function calculates the magnitude (length) of vector a:

    magnitude_a = math.sqrt(sum(x * x for x in a))

        For a = [1, 2]:

        1 * 1 = 1
        2 * 2 = 4

        1 + 4 = 5

        sqrt(5) = 2.236

    Therefore:

        magnitude_a = 2.236

    The same calculation is performed for vector b:

        b = [3, 4]

        3 * 3 = 9
        4 * 4 = 16

        9 + 16 = 25

        sqrt(25) = 5

    Therefore:

        magnitude_b = 5

    The function then checks whether either magnitude is zero:

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

    This is necessary because the final calculation divides by the magnitudes. 
    Dividing by zero would cause an error.

    Finally, the function calculates cosine similarity:

    return dot_product / (magnitude_a * magnitude_b)

    Using our values:

        11 / (2.236 * 5)
        = 11 / 11.180
        ≈ 0.984

    Therefore:

        cosine_similarity([1, 2], [3, 4])
        ≈ 0.984

    A cosine similarity close to 1 means the vectors point in very similar directions. 
    A value close to 0 means they are not very similar, and a value close to -1 means they 
    point in opposite directions.

    In a semantic memory system, the vectors can be embeddings. 
    For example, the user query "What is my name?" is converted into an embedding vector, 
    and a stored memory such as "The user's name is Vijay" is also converted into an embedding vector. 
    Cosine similarity compares these two vectors to determine how semantically similar they are.

    The important point is that cosine similarity does not directly compare the words. 
    It compares the numerical vectors representing the text.
"""