import streamlit as st
import pickle
import matplotlib.pyplot as plt
import pandas as pd

# Function to load embeddings from a pickle file
def load_embeddings(uploaded_file):
    embeddings = pickle.load(uploaded_file)
    return embeddings

# Streamlit app
def main():
    st.title("Embeddings Visualization")

    # File uploader to load the pickle file
    uploaded_file = st.file_uploader("Choose a pickle file", type="pkl")

    if uploaded_file is not None:
        embeddings = load_embeddings(uploaded_file)
        
        # Assuming embeddings is a dictionary with keys as labels and values as embedding vectors
        if isinstance(embeddings, dict):
            data = pd.DataFrame(embeddings).T
        else:
            data = pd.DataFrame(embeddings)

        st.write("Loaded Embeddings:")
        st.write(data.head())

        # Determine if embeddings are 2D or 3D
        if data.shape[1] == 2:
            plot_2d_embeddings(data)
        elif data.shape[1] == 3:
            plot_3d_embeddings(data)
        else:
            st.write("Embeddings must be 2D or 3D for visualization.")

# Function to plot 2D embeddings
def plot_2d_embeddings(data):
    fig, ax = plt.subplots()
    ax.scatter(data.iloc[:, 0], data.iloc[:, 1])
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.set_title('2D Embeddings')
    st.pyplot(fig)

# Function to plot 3D embeddings
def plot_3d_embeddings(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2])
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.set_zlabel('Dimension 3')
    ax.set_title('3D Embeddings')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
