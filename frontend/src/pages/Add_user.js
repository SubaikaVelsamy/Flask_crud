import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddUser() {
  const [full_name, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleSubmit = e => {
    e.preventDefault();

    fetch("/api/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ full_name, mobile, email })
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to save");
        return res.json();
      })
      .then(() => {
        alert("User saved");
        navigate("/"); // redirect to users list
      })
      .catch(err => alert(err.message));
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Add User</h2>

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

        <button type="submit">Save</button>
      </form>
    </div>
  );
}

export default AddUser;
