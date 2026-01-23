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
            <td>Action</td>
          </tr>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.full_name}</td>
              <td>{user.mobile}</td>
              <td>{user.email}</td>
              <td><Link to={`/edit/${user.id}`}>Edit</Link>&nbsp;&nbsp;<button onClick={() => handleDelete(user.id)}>Delete</button></td>
            </tr>
          ))}
        </table>
    </div>
  );
}

export default Users;
