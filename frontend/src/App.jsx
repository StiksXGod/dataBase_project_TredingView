import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UserProfilePage from './pages/UserProfilePage';
import AddAssetPage from './pages/AddAssetPage'; // убедитесь, что путь импорта верный
import AllAssetsPage from './pages/AllAssetsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/id/:id" element={<UserProfilePage />} />
        <Route path="/id/:id/add" element={<AddAssetPage />} />
        <Route path="/" element={<LoginPage />} />
        <Route path="/assets" element={<AllAssetsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
