import { useState, useEffect } from 'react'
import axios from 'axios'
import Step1_Context from './components/Step1_Context'
import EvaluationStep from './components/EvaluationStep'

function App() {
  const [step, setStep] = useState(0); // 0: Init, 1: Context, 2: See, 3: Think, 4: Wonder, 5: Done
  const [sessionData, setSessionData] = useState(null);
  const [allEvaluations, setAllEvaluations] = useState({});
  const [feedbackCache, setFeedbackCache] = useState({}); // { see: [], think: [], wonder: [] }

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  // Init Data on Mount
  useEffect(() => {
    // Check local storage for session
    const savedSession = localStorage.getItem("saved_session");
    if (savedSession) {
      console.log("Restoring session from storage...");
      const parsed = JSON.parse(savedSession);

      // Check for error states in cached session
      if (parsed.image_url && (parsed.image_url.includes("Error") || parsed.image_url.includes("placehold.co"))) {
        console.log("Found broken session, discarding and refreshing...");
        localStorage.removeItem("saved_session");
        refreshSession();
      } else {
        setSessionData(parsed);
        setStep(1);
      }
    } else {
      console.log("No saved session, fetching new...");
      refreshSession();
    }
  }, []);

  const refreshSession = async () => {
    try {
      setStep(0);
      setFeedbackCache({}); // Reset cache on new session
      const res = await axios.get(`${API_URL}/generate-session`);
      // Structure: { image_url, student_response: { see, think, wonder } }

      setSessionData(res.data);
      localStorage.setItem("saved_session", JSON.stringify(res.data));
      setStep(1); // Go to Context Step
    } catch (e) {
      console.error("Failed to init session", e);
      alert("세션을 불러오는데 실패했습니다. 백엔드 서버가 실행 중인지 확인해주세요.");
    }
  };

  const startNewSession = () => {
    localStorage.removeItem("saved_session");
    setAllEvaluations({});
    setFeedbackCache({});
    refreshSession();
  };

  const handleEvaluationSubmit = (stage, evaluations) => {
    // stage comes in as "See", "Think", "Wonder" from props
    setAllEvaluations(prev => ({ ...prev, [stage]: evaluations }));

    if (step < 4) {
      setStep(step + 1);
    } else {
      // Final Submit
      submitFinalData(evaluations);
    }
  };

  const handleFeedbackGenerated = (stage, newFeedbacks) => {
    setFeedbackCache(prev => ({ ...prev, [stage]: newFeedbacks }));
  };

  const submitFinalData = async (lastEvaluations) => {
    // 1. Merge last step evaluations into allEvaluations
    const completeEvaluations = {
      ...allEvaluations,
      Wonder: lastEvaluations // Ensure key matches 'Wonder' stage
    };

    // 2. Enhance evaluations with feedback text from cache
    // We need to transform the structure for the backend
    const enrichedEvaluations = {};

    // Stages: 'See', 'Think', 'Wonder'
    ['See', 'Think', 'Wonder'].forEach(stage => {
      const stageEvals = completeEvaluations[stage] || {};
      const stageFeedbacks = feedbackCache[stage] || [];

      enrichedEvaluations[stage] = {};

      stageFeedbacks.forEach(fb => {
        const modelId = fb.model_id;
        const userEval = stageEvals[modelId] || { score: 0, comment: "" };

        enrichedEvaluations[stage][modelId] = {
          score: Number(userEval.score),
          comment: userEval.comment || "",
          feedback_text: fb.feedback_text // INCLUDE THE FEEDBACK TEXT!
        };
      });
    });

    const finalPayload = {
      session_id: crypto.randomUUID(),
      ...sessionData,
      evaluations: enrichedEvaluations
    };

    console.log("Submitting Final Data:", finalPayload);
    try {
      await axios.post(`${API_URL}/submit-evaluation`, finalPayload);
      setStep(5); // Completion Screen only on success
    } catch (error) {
      console.error("Submission failed:", error);
      alert("데이터 저장 중 오류가 발생했습니다. 개발자 도구 콘솔을 확인해주세요.");
      setStep(5);
    }
  };

  if (step === 0) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md px-6">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-6"></div>
          <h1 className="text-2xl font-semibold text-gray-700 mb-3">사고 루틴에 따른 학생 응답을 불러오고 있습니다.</h1>
          <p className="text-gray-500 text-base">잠시만 기다려 주십시오.</p>
        </div>
      </div>
    );
  }

  if (step === 5) {
    return (
      <div className="h-screen flex items-center justify-center bg-green-50">
        <div className="text-center p-12 bg-white rounded-xl shadow-2xl max-w-lg mx-6">
          <div className="mb-6">
            <svg className="w-20 h-20 text-green-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-green-600 mb-4">평가가 완료되었습니다!</h1>
          <p className="text-gray-700 text-lg mb-8">교육 전문가로서 소중한 피드백 감사합니다.</p>
          <button
            onClick={() => startNewSession()}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700 transition-colors"
          >
            새로운 응답 평가하기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 font-sans">
      {/* Navbar */}
      <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">사고 루틴 평가 플랫폼 </h1>
        <div className="flex space-x-2">
          {[1, 2, 3, 4].map(s => (
            <div key={s} className={`h-2 w-8 rounded ${step >= s ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
          ))}
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto mt-6 bg-white rounded-xl shadow-lg min-h-[80vh] overflow-hidden">
        {step === 1 && (
          <Step1_Context
            stimulusUrl={sessionData.image_url}
            studentResponse={sessionData.student_response}
            onNext={() => setStep(2)}
          />
        )}
        {step === 2 && (
          <EvaluationStep
            stage="See"
            studentText={sessionData.student_response.see}
            fullStudentResponse={sessionData.student_response}
            onNext={handleEvaluationSubmit}
            onBack={() => setStep(1)}
            cachedFeedback={feedbackCache['See']}
            onFeedbackGenerated={handleFeedbackGenerated}
          />
        )}
        {step === 3 && (
          <EvaluationStep
            stage="Think"
            studentText={sessionData.student_response.think}
            fullStudentResponse={sessionData.student_response}
            onNext={handleEvaluationSubmit}
            onBack={() => setStep(2)}
            cachedFeedback={feedbackCache['Think']}
            onFeedbackGenerated={handleFeedbackGenerated}
          />
        )}
        {step === 4 && (
          <EvaluationStep
            stage="Wonder"
            studentText={sessionData.student_response.wonder}
            fullStudentResponse={sessionData.student_response}
            onNext={handleEvaluationSubmit}
            onBack={() => setStep(3)}
            isLastStep={true}
            cachedFeedback={feedbackCache['Wonder']}
            onFeedbackGenerated={handleFeedbackGenerated}
          />
        )}
      </main>
    </div>
  )
}

export default App
