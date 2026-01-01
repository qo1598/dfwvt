import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EvaluationStep = ({ stage, studentText, fullStudentResponse, onNext, onBack, isLastStep, accessCode, cachedFeedback, onFeedbackGenerated }) => {
    const [loading, setLoading] = useState(!cachedFeedback);
    const [feedbacks, setFeedbacks] = useState(cachedFeedback || []);
    const [evaluations, setEvaluations] = useState({});

    useEffect(() => {
        if (cachedFeedback && cachedFeedback.length > 0) {
            setFeedbacks(cachedFeedback);
            setLoading(false);
            return;
        }

        const fetchFeedbacks = async () => {
            try {
                setLoading(true);
                const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

                const response = await axios.post(`${API_URL}/generate-feedback`, {
                    student_response: fullStudentResponse,
                    stage: stage.toLowerCase()
                }, {
                    headers: { 'x-access-code': accessCode }
                });

                const newFeedbacks = response.data.feedbacks;
                setFeedbacks(newFeedbacks);
                if (onFeedbackGenerated) {
                    onFeedbackGenerated(stage, newFeedbacks);
                }
            } catch (error) {
                console.error("Error fetching feedbacks:", error);
                setFeedbacks([
                    { model_id: "error", model_name: "Error", feedback_text: "피드백을 불러오지 못했습니다." }
                ]);
            } finally {
                setLoading(false);
            }
        };

        fetchFeedbacks();
    }, [stage]);

    const handleEvaluationChange = (modelId, field, value) => {
        setEvaluations(prev => ({
            ...prev,
            [modelId]: {
                ...prev[modelId],
                [field]: value
            }
        }));
    };

    const isFormValid = () => {
        // For pilot: always allow proceeding, no strict validation
        return true;
    };

    return (
        <div className="flex flex-col h-full overflow-y-auto p-6 space-y-6">
            {/* Header */}
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold mb-2">루틴 단계: {stage.toUpperCase()}</h2>
                <div className="bg-gray-50 p-4 border rounded mt-2">
                    <span className="text-sm font-bold text-gray-500 uppercase">학생 응답</span>
                    <p className="text-lg text-gray-800 mt-1">"{studentText}"</p>
                </div>
            </div>

            {/* Feedback Cards Grid */}
            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {[1, 2, 3].map((idx) => (
                        <div key={idx} className="bg-white rounded-lg shadow border flex flex-col">
                            <div className="p-6 bg-gray-50 border-b flex-grow">
                                <div className="flex flex-col items-center justify-center py-8">
                                    <div className="animate-spin rounded-full h-12 w-12 border-b-3 border-blue-600 mb-4"></div>
                                    <p className="text-sm font-medium text-gray-600">피드백 {idx}</p>
                                    <p className="text-xs text-gray-500 mt-2">불러오는 중...</p>
                                </div>
                            </div>
                            <div className="p-4 space-y-4 bg-white opacity-50">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        평가 점수 (0-10)
                                    </label>
                                    <div className="w-full h-2 bg-gray-200 rounded-lg"></div>
                                    <div className="text-right text-sm font-bold text-gray-400 mt-1">
                                        - / 10
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        교사 코멘트
                                    </label>
                                    <div className="w-full h-20 bg-gray-100 rounded border border-gray-200"></div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {feedbacks.map((fb, idx) => (
                        <div key={fb.model_id} className="bg-white rounded-lg shadow border flex flex-col">
                            <div className="p-4 bg-gray-50 border-b flex-grow">
                                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 block">
                                    피드백 {idx + 1}
                                </span>
                                <p className="text-gray-700 italic">
                                    "{fb.feedback_text}"
                                </p>
                                {/* Blind Test: Hiding model name */}
                                {/* <p className="text-xs text-gray-300 mt-4 text-right">{fb.model_name}</p> */}
                            </div>

                            <div className="p-4 space-y-4 bg-white">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        평가 점수 (0-10)
                                    </label>
                                    <input
                                        type="range"
                                        min="0"
                                        max="10"
                                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                                        value={evaluations[fb.model_id]?.score || 0}
                                        onChange={(e) => handleEvaluationChange(fb.model_id, 'score', e.target.value)}
                                    />
                                    <div className="text-right text-sm font-bold text-blue-600">
                                        {evaluations[fb.model_id]?.score || 0} / 10
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        교사 코멘트
                                    </label>
                                    <textarea
                                        className="w-full border rounded p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                                        rows="3"
                                        placeholder="교육 전문가로서 피드백에 대한 평가와 해당 점수를 부여한 이유를 적어주세요."
                                        value={evaluations[fb.model_id]?.comment || ""}
                                        onChange={(e) => handleEvaluationChange(fb.model_id, 'comment', e.target.value)}
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Navigation */}
            <div className="pt-6 flex justify-between items-center">
                <button
                    onClick={onBack}
                    className="text-gray-600 hover:text-gray-900 font-medium px-4"
                >
                    ← 이전 단계로
                </button>
                {loading && (
                    <p className="text-sm text-blue-600 font-medium">
                        AI 피드백을 생성하고 있습니다...
                    </p>
                )}
                <button
                    onClick={() => onNext(stage, evaluations)}
                    disabled={!isFormValid() || loading}
                    className={`font-bold py-3 px-8 rounded-lg shadow transition-colors ${
                        loading 
                            ? 'bg-gray-400 cursor-not-allowed text-white'
                            : isLastStep
                                ? 'bg-green-600 hover:bg-green-700 text-white'
                                : 'bg-blue-600 hover:bg-blue-700 text-white'
                        }`}
                >
                    {isLastStep ? "제출하기" : "다음 단계로 →"}
                </button>
            </div>
        </div>
    );
};

export default EvaluationStep;
