
ADET: REST API LAB ACTIVITY | BSIT 3B | Alcayde, Armero, Dayto
# ARTIST_API_REST : Artist API & Management System

<br>
<h3>✱ INSTALLATION & SETUP</h3>
<br>

<ol>

  <li>
    <b>Database:</b>
    <ul>
      <li>Import the <code>database.sql</code> file into your <b>PHPMyAdmin</b>.</li>
      <li>Ensure the database name is set to <code>art_db</code>.</li>
    </ul>
  </li>

  <li>
    <b>Server:</b>
    <ul>
      <li>Place <code>api.php</code> and <code>index.html</code> into your XAMPP <code>htdocs/school-app/</code> folder.</li>
      <li>Open the XAMPP Control Panel and ensure <b>Apache</b> and <b>MySQL</b> are running.</li>
    </ul>
  </li>

  <li>
    <b>Python Client:</b>
    <ul>
      <li>Install dependencies: <code>pip install requests</code></li>
      <li>Run the client: <code>python admin_tool.py</code></li>
    </ul>
  </li>

</ol>

<br>

> **DEFAULT PASSWORD:** The Admin Password is `1`

---

<h3>✱ FEATURES</h3>
<br>

<ul>
  <li><b>Public Portal:</b> Users can search for verified artists or request to join the marketplace.</li>
  <li><b>Admin Dashboard:</b> Secure login required to Approve, Edit, or Delete artist profiles.</li>
  <li><b>Two-Stage Registration:</b> Applications are held in a <code>pending</code> state until an Admin approves them.</li>
  <li><b>Multi-Client Support:</b> Includes a modern Web UI and a Python CLI tool.</li>
  <li><b>Security:</b> Header-based authentication (<code>X-Admin-Token</code>) for all administrative actions.</li>
  <li><b>Error Handling:</b> Robust validation for duplicate usernames and incorrect credentials.</li>
</ul>
