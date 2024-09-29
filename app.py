import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# main layout
st.set_page_config(page_title="Data Job Analysis", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center; font-size: 64px; color: lightblue; margin-bottom: 40px;'>
        Welcome to Data Job Analysis
    </h1>
    """,
    unsafe_allow_html=True
)

# navigation
navigation_option = ['Job count analysis',
                     'Top 10', 'Monthly trend', 'Salary analysis']


analysis_option = st.sidebar.radio("What's to know", navigation_option)

# cleaned dataframe
df = pd.read_pickle('cleaned_df.pkl')

# dropdown selection
all_job_titles = df['Job title'].unique().tolist()
all_job_titles.insert(0, 'All job')

# function for dynamic role


def job_title_switcher(job_title):
    if job_title == "All job":
        return df.copy()
    else:
        return df[df['Job title'] == job_title]


# custom design for pie chat
def custom_pie_params():
    return {
        'color': 'white',
        'fontsize': 12,
        'fontweight': 'bold'
    }


if analysis_option == 'Job count analysis':

    # Job title by number of jobs
    # -----------------------------
    df_job_title = pd.DataFrame(df['Job title'].value_counts()).reset_index()
    df_job_title.columns = ["Job title", "Number of jobs"]

    st.title("Number of jobs by title")
    chart = alt.Chart(df_job_title).mark_bar().encode(
        y=alt.Y('Job title:N',
                sort='-x',  # Sort by 'count'
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=500)),
        x=alt.X('Number of jobs:Q',
                title='Number of jobs',
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=500)),
        color=alt.Color('Number of jobs:Q', scale=alt.Scale(
            scheme='blues'), legend=None),  # Color based on count
    ).properties(
        width=900,
        height=600
    )

    st.altair_chart(chart)

    # Remote job ratio
    # ------------------------

    col1, col2, col3, col4 = st.columns(4)  # shaping the selectbox

    with col1:
        st.title("Remote ratio")
        job_title_remote = st.selectbox(
            "Select a Job Title", all_job_titles, key="Remote")

    df_remote = job_title_switcher(job_title_remote)[
        'Remote or On-site'].value_counts(normalize=True)

    pie1, pie2 = st.columns(2)

    with pie1:
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        fig1.patch.set_alpha(.05)  # Transparent figure background
        ax1.set_facecolor('none')  # Transparent axis background
        ax1.pie(
            df_remote,
            labels=['On-site', 'Remote'],
            autopct=lambda p: f'{p:.1f}%',
            startangle=20,
            explode=[0, .05],
            textprops=custom_pie_params()
        )
        ax1.legend()
        ax1.axis('equal')
        st.pyplot(fig1)

        # Degree relevancy
        # ----------------------

        with col3:
            st.title("Degree relevancy")
            job_title_degree = st.selectbox(
                "Select a Job Title", all_job_titles, key="Degree")
        df_degree = job_title_switcher(job_title_degree)[
            'Degree required or not'].value_counts(normalize=True)

        with pie2:
            fig2, ax2 = plt.subplots(figsize=(10, 6))

            fig2.patch.set_alpha(.05)  # Transparent figure background
            ax2.set_facecolor('none')  # Transparent axis background
            ax2.pie(
                df_degree,
                labels=['Not required', 'Required'],
                autopct=lambda p: f'{p:.1f}%',
                startangle=20,
                explode=[0, .05],
                textprops=custom_pie_params()
            )
            ax2.legend()
            ax2.axis('equal')
            st.pyplot(fig2)

if analysis_option == 'Top 10':
    # Top 10 mediums by number of jobs
    # -----------------------------------

    st.title('Top 10 mediums by number of jobs')
    col1, col2, col3, col4 = st.columns(4)  # shaping the selectbox
    with col1:
        job_title_medium = st.selectbox(
            "Select a Job Title", all_job_titles, key="Medium")

    top10_medium_for_role = pd.DataFrame(job_title_switcher(job_title_medium)['Medium']
                                         .value_counts()).reset_index().head(10)
    top10_medium_for_role.columns = [
        'Job medium', f'Number of {job_title_medium} job']

    chart = alt.Chart(top10_medium_for_role).mark_bar().encode(
        y=alt.Y('Job medium:N',
                sort='-x',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=200)),
        x=alt.X(f'Number of {job_title_medium} job', title=None, axis=alt.Axis(
            labelFontSize=18, grid=False, labelLimit=500)),
        color=alt.Color(f'Number of {job_title_medium} job',
                        scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        width=900,
        height=600
    )

    st.altair_chart(chart)

    # Top 10 country by number of jobs
    # ------------------------------------

    st.title('Top 10 countries by Number of jobs')
    col1, col2, col3, col4 = st.columns(4)  # shaping the selectbox
    with col1:
        job_title_country = st.selectbox(
            "Select a Job Title", all_job_titles, key="Country")

    top10_country_for_role = pd.DataFrame(job_title_switcher(job_title_country)['Job Country']
                                          .value_counts()).reset_index().head(10)
    top10_country_for_role.columns = [
        'Country', 'Number of jobs']

    chart = alt.Chart(top10_country_for_role).mark_bar().encode(
        y=alt.Y('Country:N',
                sort='-x',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=200)),
        x=alt.X('Number of jobs', title=None, axis=alt.Axis(
            labelFontSize=18, grid=False, labelLimit=500)),
        color=alt.Color('Number of jobs', scale=alt.Scale(
            scheme='blues'), legend=None)
    ).properties(
        width=900,
        height=600
    )

    st.altair_chart(chart)

    # Top 10 company by number of jobs
    # -----------------------------------

    st.title(f'Top 10 hiring companies by number of jobs')
    col1, col2, col3, col4 = st.columns(4)  # shaping the selectbox
    with col1:
        job_title_company = st.selectbox(
            "Select a Job Title", all_job_titles, key="Company")

    top_10_company_hiring = pd.DataFrame(job_title_switcher(job_title_company)['Company Name']
                                         .str.strip()
                                         .value_counts()
                                         .head(10)).reset_index()
    top_10_company_hiring.columns = ['Company name', 'Number of jobs hired']

    chart = alt.Chart(top_10_company_hiring).mark_bar().encode(
        y=alt.Y('Company name',
                sort='-x',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=200)),
        x=alt.X('Number of jobs hired',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=500)),
        color=alt.Color('Number of jobs hired',
                        scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        width=900,
        height=600
    )

    st.altair_chart(chart)

    # Top 10 skills
    # -----------------------------------

    st.title("Top 10 skills by mentioned frequency in the job description")
    col1, col2, col3, col4 = st.columns(4)  # shaping the selectbox
    with col1:
        job_title_skills = st.selectbox(
            "Select a Job Title", all_job_titles, key="Skills")

    top_10_skills = pd.DataFrame(
        job_title_switcher(job_title_skills)['Job Skills'].
        explode().
        value_counts().
        head(10)).reset_index()
    top_10_skills.columns = ['Skill name', 'Number of skill required']

    # Create a funnel chart with Plotly
    fig = px.funnel(top_10_skills,
                    y='Skill name',
                    x='Number of skill required',
                    )

    fig.update_layout(
        width=900,
        height=600,
        yaxis=dict(title=None, tickfont=dict(size=24)),
        xaxis=dict(title=None, tickfont=dict(size=24)),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_traces(
        textfont=dict(size=16, color='black', family='Arial', weight='bold')
    )
    # Display in Streamlit
    st.plotly_chart(fig)


if analysis_option == 'Monthly trend':

    # Monthly trend by number of jobs
    # ------------------------------------

    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]  # for sorting by month

    st.title('Monthly trends by number of jobs')

    col1, col2, col3, col4 = st.columns(4)  # shaping the selectbox
    with col1:
        job_title_month = st.selectbox(
            "Select a Job Title", all_job_titles, key="Month")

    df_job_trend_month = pd.DataFrame(job_title_switcher(job_title_month).groupby(
        by='Job Month')['Job title'].count()).reset_index()
    df_job_trend_month.columns = ['Job posted month', 'Number of jobs']

    # Create the line chart with circle markers
    line = alt.Chart(df_job_trend_month).mark_line().encode(
        y=alt.Y('Number of jobs',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=200)),
        x=alt.X('Job posted month:N',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False,
                              labelLimit=500, labelAngle=45),
                sort=months_order),
    ).properties(
        width=700,
        height=600
    )

    # Add circle markers to each point on the line
    points = alt.Chart(df_job_trend_month).mark_circle(size=80).encode(
        y=alt.Y('Number of jobs'),
        x=alt.X('Job posted month:N',
                sort=months_order),
    )

    # Combine the line and circle charts
    chart = line + points

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


if analysis_option == 'Salary analysis':
    # Avg. salary by job titles
    # -----------------------------------

    st.title('Average salary by job titles')

    mean_salary = pd.DataFrame((
        df.groupby(by='Job title')['Salary Year Avg']
        .mean()
        .apply(lambda x: int(x))
        .sort_values(ascending=False)
    )).reset_index()

    chart = alt.Chart(mean_salary).mark_bar().encode(
        y=alt.Y('Job title',
                sort='-x',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=200)),
        x=alt.X('Salary Year Avg',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=500)),
        color=alt.Color('Salary Year Avg',
                        scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        width=900,
        height=600
    )

    st.altair_chart(chart)

    # Avg. salary by job titles
    # -----------------------------------
    df_salary_country = df[['Job Country', 'Salary Year Avg']].dropna(
        subset='Salary Year Avg')
    country_counts = df_salary_country['Job Country'].value_counts()
    # at least 50 salary value check
    countries_withatleast_50_values = country_counts[country_counts.values > 50].index

    filtered_country = df_salary_country[df_salary_country['Job Country'].isin(
        countries_withatleast_50_values)]
    df_avg_salary_country = pd.DataFrame(
        filtered_country
        .groupby('Job Country')['Salary Year Avg']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    ).reset_index()

    st.title('Average salary by countries')
    chart = alt.Chart(df_avg_salary_country).mark_bar().encode(
        y=alt.Y('Job Country',
                sort='-x',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=200)),
        x=alt.X('Salary Year Avg',
                title=None,
                axis=alt.Axis(labelFontSize=18, grid=False, labelLimit=500)),
        color=alt.Color('Salary Year Avg',
                        scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        width=900,
        height=600
    )

    st.altair_chart(chart)
