import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Login from "./components/auth/Login";
import Signup from "./components/auth/Signup";
import Home from "./pages/Home";
import QuestionnaireTest from "./pages/questionnaire/Test";
import QuestionnaireResult from "./pages/questionnaire/Result";
import TextAnalyze from "./pages/text/Analyze";
import TextResult from "./pages/text/Result";
import TwitterAnalyze from "./pages/twitter/Analyze";
import TwitterResult from "./pages/twitter/Result";
import QuestionnaireHistory from "./pages/questionnaire/History";
import TextHistory from "./pages/text/History";
import TwitterHistory from "./pages/twitter/History";
import ToastProvider from './components/shared/ToastProvider';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider />
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />

          <Route
            path="/questionnaire/test"
            element={
              <ProtectedRoute>
                <QuestionnaireTest />
              </ProtectedRoute>
            }
          />

          <Route
            path="/questionnaire/result/:id"
            element={
              <ProtectedRoute>
                <QuestionnaireResult />
              </ProtectedRoute>
            }
          />

          <Route
            path="/questionnaire/history"
            element={
              <ProtectedRoute>
                <QuestionnaireHistory />
              </ProtectedRoute>
            }
          />

          <Route
            path="/text/analyze"
            element={
              <ProtectedRoute>
                <TextAnalyze />
              </ProtectedRoute>
            }
          />

          <Route
            path="/text/result/:id"
            element={
              <ProtectedRoute>
                <TextResult />
              </ProtectedRoute>
            }
          />

          <Route
            path="/text/history"
            element={
              <ProtectedRoute>
                <TextHistory />
              </ProtectedRoute>
            }
          />

          <Route
            path="/twitter/analyze"
            element={
              <ProtectedRoute>
                <TwitterAnalyze />
              </ProtectedRoute>
            }
          />

          <Route
            path="/twitter/result/:id"
            element={
              <ProtectedRoute>
                <TwitterResult />
              </ProtectedRoute>
            }
          />

          <Route
            path="/twitter/history"
            element={
              <ProtectedRoute>
                <TwitterHistory />
              </ProtectedRoute>
            }
          />

          {/* Redirect unknown routes */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
