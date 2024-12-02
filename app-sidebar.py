import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64

# Fungsi untuk menghitung skor berdasarkan kategori
def calculate_scores(df, answers):
    scores = df[['cat']].copy()
    scores['score'] = answers
    total_scores = scores.groupby('cat')['score'].sum().to_dict()
    return total_scores

# Fungsi untuk membuat grafik
def plot_category_distribution(df, answered_count):
    # Menyaring data sesuai jumlah pertanyaan yang dijawab
    filtered_df = df.iloc[:answered_count]
    category_counts = filtered_df['cat'].value_counts()

    # Membuat grafik
    fig, ax = plt.subplots()
    category_counts.plot(kind='bar', color=['#6baed6', '#fd8d3c', '#74c476'], ax=ax)
    ax.set_title(f"Distribusi Kategori ({answered_count} Pertanyaan Dijawab)")
    ax.set_xlabel("Kategori")
    ax.set_ylabel("Jumlah Pertanyaan")
    ax.set_xticks(range(len(category_counts)))
    ax.set_xticklabels(['Stress (S)', 'Anxiety (A)', 'Depression (D)'])
    ax.bar_label(ax.containers[0])  # Menambahkan label jumlah pada tiap bar
    
    return fig

# Membuat aplikasi Streamlit
def main():
    # Load dataset
    file_path = "DASS21_v1.csv"  # Sesuaikan dengan lokasi dataset Anda
    df = pd.read_csv(file_path)

    # Sidebar untuk navigasi
    st.sidebar.title("📋 **DASS-21 Assessment**")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigasi Utama")
    menu = st.sidebar.selectbox(
        "Pilih Halaman",
        ["🏠 Home", "📊 Dataset", "🧠 Prediksi"]
    )

    # Sidebar informasi tambahan
    st.sidebar.markdown("---")
    st.sidebar.subheader("Tentang")
    st.sidebar.info(
        """
        Aplikasi ini didasarkan pada **DASS-21**, 
        yang membantu mengukur tingkat **Stress**, **Anxiety**, dan **Depression**.
        """
    )

    # Home Page
    if menu == "🏠 Home":
        st.title("🏠 Aplikasi Prediksi Tingkat Anxiety DASS-21")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Selamat Datang!
            Aplikasi ini dirancang untuk membantu Anda menilai tingkat **Stress**, **Anxiety**, dan **Depression** berdasarkan kuesioner **DASS-21**.
            """, unsafe_allow_html=True)
        with col2:
            st.image("anxiety.jpg", caption="DASS-21 Assessment", use_column_width=True)

    # Dataset Page
    elif menu == "📊 Dataset":
        st.title("📊 Dataset DASS-21")
        st.markdown("Berikut adalah dataset dari kuesioner **DASS-21**.")
        st.dataframe(df)

    # Prediksi Page
    elif menu == "🧠 Prediksi":
        st.title("🧠 Prediksi Tingkat Anxiety dengan DASS-21")
        st.write("Jawab pertanyaan berikut sesuai dengan kondisi Anda:")
        user_answers = []

        # Slider untuk memilih jumlah pertanyaan yang dijawab
        max_questions = len(df)
        answered_count = st.slider("Jumlah Pertanyaan yang Dijawab:", 1, max_questions, value=max_questions)

        # Input jawaban untuk setiap pertanyaan
        for index, row in df.iterrows():
            if index >= answered_count:
                break
            answer = st.radio(
                f"{row['qno']}. {row['qtext']}",
                options=[0, 1, 2, 3],
                index=0,
                horizontal=True
            )
            user_answers.append(answer)

        # Tampilkan grafik distribusi kategori
        st.markdown("### 📈 Grafik Distribusi Kategori")
        fig = plot_category_distribution(df, answered_count)
        st.pyplot(fig)

        # Prediksi skor
        if st.button("💡 Lihat Hasil"):
            total_scores = calculate_scores(df.iloc[:answered_count], user_answers)
            st.success("Berikut adalah hasil Anda:")
            for category, score in total_scores.items():
                st.write(f"**{category.capitalize()}**: {score}")

            # Klasifikasi berdasarkan skor
            st.write("### Kategori Hasil:")
            thresholds = {"s": 14, "a": 7, "d": 10}
            for category, score in total_scores.items():
                level = (
                    "Ringan"
                    if score <= thresholds[category]
                    else "Sedang"
                    if score <= thresholds[category] * 2
                    else "Berat"
                )
                st.write(f"- **{category.capitalize()}**: {level}")

if __name__ == "__main__":
    main()
