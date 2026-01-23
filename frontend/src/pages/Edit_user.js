import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

function EditUser() {
  const { id } = useParams();  // get user id from URL
  const navigate = useNavigate();

  const [full_name, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [email, setEmail] = useState("");

  // 1️⃣ Fetch user data to pre-fill form
  useEffect(() => {
    fetch(`/api/user/${id}`)
      .then(res => res.json())
      .then(data => {
        setFullName(data.full_name);
        setMobile(data.mobile);
        setEmail(data.email);
      });
  }, [id]);

  // 2️⃣ Submit updated data
  const handleSubmit = e => {
    e.preventDefault();

    fetch(`/api/edit/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ full_name, mobile, email })
    })
      .then(res => res.json())
      .then(() => {
        alert("User updated successfully");
        navigate("/"); // redirect back to users list
      })
      .catch(err => alert(err.message));
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Edit User</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <input
            placeholder="Full Name"
            value={full_name}
            onChange={e => setFullName(e.target.value)}
            required
          />
        </div>

        <div>
          <input
            placeholder="Mobile"
            value={mobile}
            onChange={e => setMobile(e.target.value)}
            required
          />
        </div>

        <div>
          <input
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <button type="submit">Update</button>
      </form>
    </div>
  );
}

export default EditUser;
