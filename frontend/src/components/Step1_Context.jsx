import React from 'react';

const Step1_Context = ({ stimulusUrl, studentResponse, onNext }) => {
  if (!studentResponse) {
    return <div className="p-10 text-center">Loading Session...</div>;
  }

  return (
    <div className="flex flex-col h-full overflow-y-auto p-6 space-y-6">
      {/* Header */}
      <div className="border-b pb-4">
        <h2 className="text-2xl font-bold mb-2">사고 루틴별 학생 응답 검토 </h2>
        <p className="text-gray-600">
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left: Stimulus */}
        <div className="bg-gray-100 rounded-lg p-4 flex items-center justify-center min-h-[400px]">
          {stimulusUrl ? (
            <img
              src={stimulusUrl}
              alt="Stimulus"
              className="max-h-[500px] object-contain rounded shadow-lg"
            />
          ) : (
            <div className="text-gray-400">이미지 생성 실패 (Generation Failed)</div>
          )}
        </div>

        {/* Right: Student Response (Whole) */}
        <div className="space-y-6">
          {/* Persona Hidden as per request */}
          {/* <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">...</div> */}

          <div className="space-y-4">
            <div className="bg-white p-4 rounded border shadow-sm">
              <span className="font-bold text-gray-700 block mb-1">SEE (관찰하기)</span>
              <p className="text-gray-800">{studentResponse.see}</p>
            </div>
            <div className="bg-white p-4 rounded border shadow-sm">
              <span className="font-bold text-gray-700 block mb-1">THINK (생각하기)</span>
              <p className="text-gray-800">{studentResponse.think}</p>
            </div>
            <div className="bg-white p-4 rounded border shadow-sm">
              <span className="font-bold text-gray-700 block mb-1">WONDER (궁금하기)</span>
              <p className="text-gray-800">{studentResponse.wonder}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Navigation */}
      <div className="pt-6 flex justify-end">
        <button
          onClick={onNext}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg shadow transition-colors"
        >
          평가 시작하기
        </button>
      </div>
    </div>
  );
};

export default Step1_Context;
