# noqa

import numpy as np
from typing import Tuple, List


class RecommendationsProcessor:
    """Процессор рекомендательной системы."""

    def __init__(
        self,
        data: np.ndarray,
        k: int = 5,
        steps: int = 500,
        alpha: float = 1e-4,
        reg_param: float = 0.8,
        verbose: bool = False,
    ) -> None:
        """
        Constructor of the class. Takes the user preferences matrix R
        and parameters for matrix factorization.

        Args:
            R (np.ndarray): The user-item preference matrix (users-questions).
            k (int): The number of latent factors for matrix factorization.
            steps (int): The number of iterations for ALS.
            alpha (float): The learning rate.
            reg_param (float): The regularization parameter.
        """
        self.verbose = verbose
        self.data = data
        self.k = k
        self.steps = steps
        self.alpha = alpha
        self.reg_param = reg_param

        # Perform matrix factorization during initialization
        self.P, self.Q = self.matrix_factorization()

    def initialize_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        """Initializes the matrices P and Q with random values.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The initialized matrices.
        """
        num_users, num_questions = self.data.shape
        # User preference matrix
        P = np.random.rand(num_users, self.k)
        # Item (question) feature matrix
        Q = np.random.rand(num_questions, self.k)
        return P, Q

    def loss_function(self, P: np.ndarray, Q: np.ndarray) -> float:
        """Computes the loss (MSE) with regularization.

        Args:
            P (np.ndarray): User preference matrix.
            Q (np.ndarray): Item (question) feature matrix.

        Returns:
            float: The computed loss value.
        """
        data_hat = np.dot(P, Q.T)

        error = (self.data - data_hat) * (self.data > 0)
        mse = np.sum(np.square(error))

        reg_term = self.reg_param * (np.linalg.norm(P) + np.linalg.norm(Q))
        return mse + reg_term

    def matrix_factorization(self) -> Tuple[np.ndarray, np.ndarray]:
        """Performs matrix factorization using Alternating Least Squares (ALS).

        Returns:
            Tuple[np.ndarray, np.ndarray]: The factorized matrices P and Q.
        """
        num_users, num_questions = self.data.shape
        P, Q = self.initialize_matrices()
        Q = Q.T  # Transpose Q for ease of computation

        # Создаем маску для известных значений
        mask = self.data > 0  # mask[i, j] = True, если R[i, j] известно

        for step in range(self.steps):
            R_hat = np.dot(P, Q)
            error_matrix = (self.data - R_hat) * mask

            P_grad = np.dot(error_matrix, Q.T) - self.reg_param * P
            Q_grad = np.dot(error_matrix.T, P) - self.reg_param * Q.T

            P += self.alpha * P_grad
            Q += self.alpha * Q_grad.T

            if self.verbose:
                if step % 100 == 0:
                    loss = self.loss_function(P, Q.T)
                    print(f"Step {step}/{self.steps}, loss: {loss}")

        return P, Q.T

    @classmethod
    def cosine_similarity(cls, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculates cosine similarity between two vectors.

        Args:
            vec1 (np.ndarray): The first vector.
            vec2 (np.ndarray): The second vector.

        Returns:
            float: The cosine similarity between the two vectors.
        """
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        return dot_product / (norm_vec1 * norm_vec2)

    @classmethod
    def predict(
        cls,
        P: np.ndarray,
        user_id: int,
        top_n: int = 3,
        verbose: bool = False,
    ) -> List[Tuple[int, float]]:
        """
        Recommends top-N users similar to the given user.

        Args:
            P (np.ndarray): User preference matrix.
            user_id (int): ID of the user to generate recommendations for.
            top_n (int): Number of recommended users.
            verbose (bool): Print log?
        """
        user_vector = P[user_id]
        similarities: List[Tuple[int, float]] = []

        for other_user_id in range(P.shape[0]):
            if other_user_id != user_id:
                similarity = cls.cosine_similarity(
                    user_vector, P[other_user_id]
                )
                similarities.append((other_user_id, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar_users = similarities[:top_n]

        if verbose:
            print(f"Top-{top_n} recommended users for User {user_id + 1}:")
            for idx, (user, similarity) in enumerate(top_similar_users):
                print(
                    f"{idx + 1}: User {user + 1} \
                        (Similarity: {similarity:.4f})"
                )

        return top_similar_users
