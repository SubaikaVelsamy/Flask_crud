import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Users() {
  const [users, setUsers] = useState([]);

  const fetchUsers = () => {
    fetch("/api/users")
      .then(res => res.json())
      .then(data => setUsers(data));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this user?")) {
      fetch(`/api/delete/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(() => {
          alert("User deleted successfully");
          fetchUsers(); // refresh the list
        });
    }
  };

  const handlePhotoChange = async (e, userId, setUsers) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("profile_photo", file);

  const res = await fetch(`http://localhost:5000/api/user/${userId}/photo`, {
    method: "PUT",
    body: formData,
  });

  const data = await res.json();

  if (res.ok) {
    // Update photo instantly in UI
    setUsers(prev =>
      prev.map(user =>
        user.id === userId
          ? { ...user, profile_photo: data.photo_url.split("/").pop() }
          : user
      )
    );
  }
};

  return (
    <div style={{ padding: "40px" }}>
      <h2>Users</h2>

      <Link to="/add" style={{ marginBottom: "20px", display: "inline-block" }}>
        ➕ Add User
      </Link>

      <table border="1">
          <tr>
            <td>Full Name</td>
            <td>Mobile</td>
            <td>Email ID</td>
            <td>Profile Photo</td>
            <td>Action</td>
          </tr>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.full_name}</td>
              <td>{user.mobile}</td>
              <td>{user.email}</td>
              <td style={{ textAlign:"center" }}>
                <img src={user.profile_photo ? `http://localhost:5000/static/uploads/${user.profile_photo}`: "http://localhost:5000/static/uploads/default.jpg"} alt="profile" width="50" height="50" style={{ borderRadius: "50%", objectFit: "cover" }}/>
                <label style={{ cursor: "pointer", color: "blue", display: "block" }}>Update<input type="file" accept="image/*" style={{ display: "none" }} onChange={(e) => handlePhotoChange(e, user.id, setUsers)}/></label>
              </td>
              <td><Link to={`/edit/${user.id}`}>Edit</Link>&nbsp;&nbsp;<button onClick={() => handleDelete(user.id)}>Delete</button></td>
            </tr>
          ))}
        </table>
    </div>
  );
}

export default Users;
