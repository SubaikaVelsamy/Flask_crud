import { Routes, Route  } from "react-router-dom";
import Users from "./pages/User";
import AddUser from "./pages/Add_user";
import EditUser from "./pages/Edit_user";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Users/>} />
      <Route path="/add" element={<AddUser/>} />
      <Route path="/edit/:id" element={<EditUser />} />
    </Routes>
  );
}

export default App;