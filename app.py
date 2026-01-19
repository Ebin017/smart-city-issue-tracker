import streamlit as st
import sqlite3
from datetime import datetime
import os

# EMAIL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import plotly.express as px
import pandas as pd



def create_table():
    """Initialize the database with required table structure"""
    conn = sqlite3.connect('issues.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    description TEXT,
                    category TEXT,
                    location TEXT,
                    image_path TEXT,
                    status TEXT,
                    date_reported TEXT
                )''')
    conn.commit()
    conn.close()


def send_issue_confirmation_email(to_email, reporter_name, issue_id, category, location, description):


    sender_email = "smartcitytracker@gmail.com"
    sender_password = "lbyahddzsmxbksla"

    if not to_email or to_email.strip() == "":
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"✅ Smart City - Issue #{issue_id} Reported Successfully"


        body_text = f"""
Hello {reporter_name},

Thank you for reporting an issue! We have received your report and it has been successfully submitted to our system.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 YOUR REPORTED ISSUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue ID:     {issue_id}
Category:     {category}
Location:     {location}
Description:  {description}
Status:       Pending

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What happens next?
⏳ Your issue is now pending review by our team.
🔧 Once we start working on it, you'll receive an update.
✅ When it's resolved, we'll notify you immediately.



We appreciate your contribution to improving our city! 🌆

Best regards,
Smart City Issue Tracker Team

---
This is an automated message. Please do not reply to this email.
        """

        msg.attach(MIMEText(body_text, 'plain'))

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email,sender_password)
            server.send_message(msg)

        return True

    except Exception as e:
        return False



def get_status_message(status):

    messages = {
        "Pending": "⏳ Your issue has been received and is awaiting review by our team.",
        "In Progress": "🔧 Great news! Our team is actively working on resolving this issue.",
        "Resolved": "✅ Excellent! This issue has been successfully resolved. Thank you for your patience!"
    }
    return messages.get(status, "Your issue status has been updated.")


def send_status_update_email(to_email, reporter_name, issue_id, category, location, new_status):


    sender_email = "smartcitytracker@gmail.com"
    sender_password = "lbyahddzsmxbksla"

    if not to_email or to_email.strip() == "":
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"🔔 Smart City - Issue #{issue_id} Update"


        body_text = f"""
Hello {reporter_name},

Good news! Your reported issue has been updated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ISSUE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue ID:     {issue_id}
Category:     {category}
Location:     {location}
New Status:   {new_status}

{get_status_message(new_status)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for helping improve our city! 🌆

Best regards,
Smart City Issue Tracker Team

---
This is an automated message. Please do not reply to this email.
        """

        msg.attach(MIMEText(body_text, 'plain'))

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True

    except smtplib.SMTPAuthenticationError:
        st.error("❌ Email authentication failed. Check credentials!")
        return False
    except Exception as e:
        st.warning(f"⚠️ Could not send email: {str(e)}")
        return False


# add function
def add_issue(name, email, description, category, location, image_file):

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Save uploaded image with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"{timestamp}_{image_file.name}"
    image_path = os.path.join("uploads", image_filename)

    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())

    date_reported = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('issues.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO issues (name, email, description, category, location, image_path, status, date_reported)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, description, category, location, image_path, "Pending", date_reported))

    issue_id = c.lastrowid

    conn.commit()
    conn.close()


    email_sent = False
    if email and email.strip() != "":
        email_sent = send_issue_confirmation_email(
            to_email=email,
            reporter_name=name,
            issue_id=issue_id,
            category=category,
            location=location,
            description=description
        )

    return issue_id, email_sent


# update function
def update_status(issue_id, new_status):


    conn = sqlite3.connect('issues.db')
    c = conn.cursor()


    c.execute("SELECT name, email, category, location FROM issues WHERE id = ?", (issue_id,))
    result = c.fetchone()

    email_sent = False

    if result:
        name, email, category, location = result


        c.execute("UPDATE issues SET status = ? WHERE id = ?", (new_status, issue_id))
        conn.commit()


        if email and email.strip() != "":
            email_sent = send_status_update_email(
                to_email=email,
                reporter_name=name,
                issue_id=issue_id,
                category=category,
                location=location,
                new_status=new_status
            )

    conn.close()
    return email_sent

#delete msg functionn
def send_issue_deleted_email(to_email, reporter_name, issue_id, category, location, description):


    # YOUR EMAIL CREDENTIALS (same as before)
    sender_email = "smartcitytracker@gmail.com"
    sender_password = "lbyahddzsmxbksla"

    # Don't send if no email provided
    if not to_email or to_email.strip() == "":
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"🗑️ Smart City - Issue #{issue_id} Removed"

        # Email body
        body_text = f"""
Hello {reporter_name},

We're writing to inform you that your reported issue has been removed from our system.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 REMOVED ISSUE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue ID:     {issue_id}
Category:     {category}
Location:     {location}
Description:  {description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This issue was removed by an administrator. This could be because:
• The issue was a duplicate
• The issue was resolved and archived
• The issue was reported in error
• The issue did not meet reporting guidelines

If you believe this was done in error, please contact us or report the issue again.

Thank you for helping improve our city! 🌆

Best regards,
Smart City Issue Tracker Team

---
This is an automated message. Please do not reply to this email.
        """

        msg.attach(MIMEText(body_text, 'plain'))

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True

    except Exception as e:
        return False


# delete function
def delete_issue(issue_id):

    conn = sqlite3.connect('issues.db')
    c = conn.cursor()


    c.execute("SELECT name, email, category, location, description, image_path FROM issues WHERE id = ?", (issue_id,))
    result = c.fetchone()

    email_sent = False

    if result:
        name, email, category, location, description, image_path = result


        if os.path.exists(image_path):
            os.remove(image_path)


        c.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
        conn.commit()


        if email and email.strip() != "":
            email_sent = send_issue_deleted_email(
                to_email=email,
                reporter_name=name,
                issue_id=issue_id,
                category=category,
                location=location,
                description=description
            )

    conn.close()
    return email_sent



def get_statistics():

    conn = sqlite3.connect('issues.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM issues")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM issues WHERE status = 'Pending'")
    pending = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM issues WHERE status = 'In Progress'")
    in_progress = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM issues WHERE status = 'Resolved'")
    resolved = c.fetchone()[0]

    conn.close()

    return total, pending, in_progress, resolved

def get_chart_data():

    try:
        conn = sqlite3.connect('issues.db')
        df = pd.read_sql("SELECT * FROM issues", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def create_pie_chart(df):

    if df.empty:
        st.warning("No data available for pie chart")
        return None

    # Count issues in each category
    category_counts = df['category'].value_counts()

    # Create pie chart
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Issues by Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    # Show percentage and label inside slices
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )

    fig.update_layout(showlegend = False)

    return fig


def create_bar_chart(df):


    if df.empty:
        st.warning("No data available for bar chart")
        return None

    # Count issues by status
    status_counts = df['status'].value_counts()

    # Define colors for each status
    colors = {
        'Pending': '#FFA500',  # Orange
        'In Progress': '#4169E1',  # Blue
        'Resolved': '#32CD32'  # Green
    }

    # Create bar chart
    fig = px.bar(
        x=status_counts.index,  # X-axis: Status names
        y=status_counts.values,  # Y-axis: Counts
        title="Issues by Status",
        labels={'x': 'Status', 'y': 'Number of Issues'},
        color=status_counts.index,  # Color by status
        color_discrete_map=colors
    )


    fig.update_layout(showlegend=False)

    return fig


def create_line_chart(df):


    if df.empty:
        st.warning("No data available for line chart")
        return None

    # Convert date column to datetime format
    df['date_reported'] = pd.to_datetime(df['date_reported'])

    # Group by date and count issues per day
    daily_counts = df.groupby(df['date_reported'].dt.date).size().reset_index(name='count')

    # Create line chart
    fig = px.line(
        daily_counts,
        x='date_reported',
        y='count',
        title="Issues Reported Over Time",
        labels={'date_reported': 'Date', 'count': 'Number of Issues'},
        markers=True  # Show dots on the line
    )

    # Customize line appearance
    fig.update_traces(
        line_color='#4169E1',  # Blue line
        line_width=3  # Thick line
    )

    return fig


def display_charts():


    # Get data from database
    df = get_chart_data()

    # Check if database has data
    if df.empty:
        st.warning("⚠️ No data available. Please report some issues first!")
        return

    #pie and bar
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = create_pie_chart(df)
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = create_bar_chart(df)
        if fig_bar:
            st.plotly_chart(fig_bar, use_container_width=True)

    # line
    fig_line = create_line_chart(df)
    if fig_line:
        st.plotly_chart(fig_line, use_container_width=True)


# ui
def main():
    st.set_page_config(page_title="Smart City Issue Tracker", page_icon="🌆", layout="wide")

    st.title("🌆 Smart City Issue Tracker")
    st.subheader("Report and View Issues in Your City")

    # Sidebar menu
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio(
        "Select an option:",
        [ "📝 Report Issue" ,"📋 View Reported Issues", "🛠️ Admin Panel","📊 Dashboard"]
    )

    # Dashboard
    if choice == "📊 Dashboard":
        st.header("📊 Dashboard Overview")

        total, pending, in_progress, resolved = get_statistics()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Issues", total)
        with col2:
            st.metric("Pending", pending)
        with col3:
            st.metric("In Progress", in_progress)
        with col4:
            st.metric("Resolved", resolved)

        st.markdown("---")

        display_charts()

        st.markdown("---")

        st.subheader("📋 Recent Issues")
        conn = sqlite3.connect('issues.db')
        c = conn.cursor()
        c.execute("SELECT * FROM issues ORDER BY date_reported DESC LIMIT 5")
        recent_issues = c.fetchall()
        conn.close()

        if recent_issues:
            for issue in recent_issues:
                with st.expander(f"Issue {issue[0]} - {issue[4]} ({issue[7]})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Reported by:** {issue[1]}")
                        st.write(f"**Email:** {issue[2] if issue[2] else 'Not provided'}")
                        st.write(f"**Description:** {issue[3]}")
                        st.write(f"**Location:** {issue[5]}")
                        st.write(f"**Reported on:** {issue[8]}")
                    with col2:
                        if os.path.exists(issue[6]):
                            st.image(issue[6], width=300)
        else:
            st.info("No issues reported yet.")

    # Report Issue
    elif choice == "📝 Report Issue":
        st.header("📝 Report an Issue")

        with st.form("issue_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Your Name *")
                email = st.text_input("Your Email *",
                                      placeholder="example@gmail.com",
                                      help="We'll send you updates about your issue")
                category = st.selectbox("Category *",
                                        ["Streetlight", "Road", "Garbage", "Water", "Other"])
                location = st.text_input("Location *")

            with col2:
                description = st.text_area("Issue Description *", height=185)

            image_file = st.file_uploader("Upload Image *", type=["jpg", "jpeg", "png"])

            # Info about email notifications
            # st.info("📧 You'll receive email updates when your issue status changes")

            submitted = st.form_submit_button("Submit Issue")

            if submitted:
                if name and email and description and category and location and image_file:
                    # Basic email validation
                    if "@" in email and "." in email:
                        issue_id, email_sent = add_issue(name, email, description, category, location, image_file)
                        st.success(f"✅ Issue {issue_id} submitted successfully!")

                        # Show email confirmation status
                        # if email_sent:
                        #     st.info(f"📧 Confirmation email sent to {email}")
                        # else:
                        #     st.warning("⚠️ Issue submitted but confirmation email failed to send")

                        # st.balloons()
                    else:
                        st.error("⚠️ Please enter a valid email address (must contain @ and .)")
                else:
                    st.error("⚠️ Please fill all required fields (*) and upload an image.")

    # View Issues
    elif choice == "📋 View Reported Issues":
        st.header("📋 Reported Issues")

        col1, col2, col3 = st.columns(3)

        with col1:
            search = st.text_input("🔍 Search", placeholder="ID,Name, location, or category")
        with col2:
            filter_category = st.selectbox("Category",
                                           ["All", "Streetlight", "Road", "Garbage", "Water", "Other"])
        with col3:
            filter_status = st.selectbox("Status", ["All", "Pending", "In Progress", "Resolved"])

        conn = sqlite3.connect('issues.db')
        c = conn.cursor()

        query = "SELECT * FROM issues WHERE 1=1"
        params = []

        if search:
            query += " AND (id like ? OR name LIKE ? OR location LIKE ? OR category LIKE ?)"
            params.extend([f"{search}",f"%{search}%", f"%{search}%", f"%{search}%"])

        if filter_category != "All":
            query += " AND category = ?"
            params.append(filter_category)

        if filter_status != "All":
            query += " AND status = ?"
            params.append(filter_status)

        query += " ORDER BY date_reported DESC"

        c.execute(query, params)
        issues = c.fetchall()
        conn.close()

        st.write(f"Found **{len(issues)}** issue(s)")
        st.markdown("---")

        if issues:
            for issue in issues:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### Issue {issue[0]} - {issue[4]}")
                    st.write(f"**Reported by:** {issue[1]}")
                    st.write(f"**Email:** {issue[2] if issue[2] else 'Not provided'}")
                    st.write(f"**Description:** {issue[3]}")
                    st.write(f"**Location:** {issue[5]}")

                    status = issue[7]
                    if status == "Pending":
                        st.markdown(f"**Status:** :orange[{status}]")
                    elif status == "In Progress":
                        st.markdown(f"**Status:** :blue[{status}]")
                    else:
                        st.markdown(f"**Status:** :green[{status}]")

                    st.write(f"**Reported on:** {issue[8]}")

                with col2:
                    image_path = os.path.abspath(issue[6])
                    if os.path.exists(image_path):
                        st.image(image_path, use_container_width=True)
                    else:
                        st.warning("Image not found")

                st.markdown("---")
        else:
            st.info("No matching issues found. Try adjusting your filters.")

    # Admin Panel
    elif choice == "🛠️ Admin Panel":
        st.header("🛠️ Admin Panel")

        if 'admin_logged_in' not in st.session_state:
            st.session_state.admin_logged_in = False

        if not st.session_state.admin_logged_in:
            password = st.text_input("Enter admin password:", type="password")

            if st.button("Login"):
                if password == "ebin123":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
        else:
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("🚪 Logout"):
                    st.session_state.admin_logged_in = False
                    st.rerun()

            st.success("Welcome, Admin!")

            total, pending, in_progress, resolved = get_statistics()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total", total)
            with col2:
                st.metric("Pending", pending)
            with col3:
                st.metric("In Progress", in_progress)
            with col4:
                st.metric("Resolved", resolved)

            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:
                search = st.text_input("🔍 Search", placeholder="ID,Name, location, or category")
            with col2:
                filter_category = st.selectbox("Category",
                                               ["All", "Streetlight", "Road", "Garbage", "Water", "Other"])
            with col3:
                filter_status = st.selectbox("Status", ["All", "Pending", "In Progress", "Resolved"])

            conn = sqlite3.connect('issues.db')
            c = conn.cursor()

            query = "SELECT * FROM issues WHERE 1=1"
            params = []

            if search:
                query += " AND (id like ? OR name LIKE ? OR location LIKE ? OR category LIKE ?)"
                params.extend([f"{search}", f"%{search}%", f"%{search}%", f"%{search}%"])

            if filter_category != "All":
                query += " AND category = ?"
                params.append(filter_category)

            if filter_status != "All":
                query += " AND status = ?"
                params.append(filter_status)

            query += " ORDER BY date_reported DESC"

            c.execute(query, params)
            issues = c.fetchall()
            conn.close()

            st.write(f"Found **{len(issues)}** issue(s)")
            st.markdown("---")
            if issues:
                for issue in issues:
                    with st.expander(f"Issue {issue[0]} - {issue[4]} ({issue[1]}) - {issue[7]}"):
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.write(f"**Name:** {issue[1]}")
                            st.write(f"**Email:** {issue[2] if issue[2] else 'Not provided'}")
                            st.write(f"**Description:** {issue[3]}")
                            st.write(f"**Category:** {issue[4]}")
                            st.write(f"**Location:** {issue[5]}")
                            st.write(f"**Reported on:** {issue[8]}")

                            new_status = st.selectbox(
                                "Update Status:",
                                ["Pending", "In Progress", "Resolved"],
                                index=["Pending", "In Progress", "Resolved"].index(issue[7]),
                                key=f"status_{issue[0]}"
                            )

                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button(f"💾 Update", key=f"update_{issue[0]}"):
                                    email_sent = update_status(issue[0], new_status)
                                    st.success(f"✅ Status updated to {new_status}")

                                    # Show email notification status
                                    if issue[2] and issue[2].strip() != "":
                                        if email_sent:
                                            st.info(f"📧 Email notification sent to {issue[2]}")
                                        else:
                                            st.warning(f"⚠️ Status updated but email failed to send")
                                    else:
                                        st.warning("⚠️ No email address on record")

                                    st.rerun()

                            with col_b:
                                if st.button(f"🗑️ Delete", key=f"delete_{issue[0]}", type="secondary"):
                                    email_sent = delete_issue(issue[0])
                                    st.success("✅ Issue deleted")

                                    # Show email notification status
                                    if issue[2] and issue[2].strip() != "":
                                        if email_sent:
                                            st.info(f"📧 Deletion notification sent to {issue[2]}")
                                        else:
                                            st.warning(f"⚠️ Issue deleted but email failed to send")
                                    else:
                                        st.warning("⚠️ Issue deleted (no email on record)")

                                    st.rerun()

                        with col2:
                            if os.path.exists(issue[6]):
                                st.image(issue[6], use_container_width=True)

            else:
                st.info("No matching issues found. Try adjusting your filters.")

if __name__ == '__main__':
    create_table()
    main()