import jsPDF from 'jspdf';

export const generateQuestionnairePDF = (prediction, insights) => {
  const doc = new jsPDF();
  const mbti = prediction.mbtiType;
  
  // Page 1: Cover
  doc.setFillColor(139, 92, 246); // Purple
  doc.rect(0, 0, 210, 297, 'F');
  
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(40);
  doc.text('MindMorph', 105, 100, { align: 'center' });
  
  doc.setFontSize(28);
  doc.text('Personality Report', 105, 120, { align: 'center' });
  
  doc.setFontSize(50);
  doc.text(mbti, 105, 160, { align: 'center' });
  
  doc.setFontSize(22);
  doc.text(insights.title, 105, 180, { align: 'center' });
  
  doc.setFontSize(12);
  const date = new Date(prediction.timestamp).toLocaleDateString();
  doc.text(`Generated: ${date}`, 105, 260, { align: 'center' });
  
  // Page 2: Overview
  doc.addPage();
  doc.setFillColor(255, 255, 255);
  doc.rect(0, 0, 210, 297, 'F');
  doc.setTextColor(0, 0, 0);
  
  doc.setFontSize(24);
  doc.text('Your Personality Type', 20, 30);
  
  doc.setFontSize(16);
  doc.text(`${mbti} - ${insights.title}`, 20, 45);
  
  doc.setFontSize(11);
  const descLines = doc.splitTextToSize(insights.description, 170);
  doc.text(descLines, 20, 60);
  
  // Confidence Scores
  let yPos = 90;
  doc.setFontSize(16);
  doc.text('Confidence Breakdown', 20, yPos);
  yPos += 10;
  
  doc.setFontSize(11);
  const labels = {
    IE: mbti[0] === 'I' ? 'Introversion' : 'Extraversion',
    NS: mbti[1] === 'N' ? 'Intuition' : 'Sensing',
    TF: mbti[2] === 'T' ? 'Thinking' : 'Feeling',
    JP: mbti[3] === 'J' ? 'Judging' : 'Perceiving'
  };
  
  Object.entries(prediction.confidence).forEach(([dim, score]) => {
    const percentage = Math.round(score * 100);
    doc.text(`${labels[dim]}: ${percentage}%`, 20, yPos);
    
    // Draw bar
    doc.setFillColor(200, 200, 200);
    doc.rect(80, yPos - 4, 100, 6, 'F');
    
    doc.setFillColor(139, 92, 246);
    doc.rect(80, yPos - 4, percentage, 6, 'F');
    
    yPos += 12;
  });
  
  // Frequency
  yPos += 10;
  doc.setFontSize(11);
  doc.text(`Population: ${insights.percentage}`, 20, yPos);
  
  // Page 3: Strengths & Weaknesses
  doc.addPage();
  doc.setFillColor(255, 255, 255);
  doc.rect(0, 0, 210, 297, 'F');
  
  doc.setFontSize(20);
  doc.text('Strengths', 20, 30);
  
  yPos = 45;
  doc.setFontSize(11);
  insights.strengths.forEach((strength, idx) => {
    doc.text(`${idx + 1}. ${strength}`, 25, yPos);
    yPos += 10;
  });
  
  yPos += 15;
  doc.setFontSize(20);
  doc.text('Growth Areas', 20, yPos);
  yPos += 15;
  
  doc.setFontSize(11);
  insights.weaknesses.forEach((weakness, idx) => {
    doc.text(`${idx + 1}. ${weakness}`, 25, yPos);
    yPos += 10;
  });
  
  // Page 4: Careers
  doc.addPage();
  doc.setFillColor(255, 255, 255);
  doc.rect(0, 0, 210, 297, 'F');
  
  doc.setFontSize(20);
  doc.text('Recommended Careers', 20, 30);
  
  yPos = 45;
  doc.setFontSize(11);
  insights.careers.forEach((career) => {
    doc.text(`• ${career}`, 25, yPos);
    yPos += 10;
  });
  
  yPos += 15;
  doc.setFontSize(20);
  doc.text('Study Habits', 20, yPos);
  yPos += 15;
  
  doc.setFontSize(11);
  insights.study_habits.forEach((habit) => {
    const lines = doc.splitTextToSize(`• ${habit}`, 165);
    doc.text(lines, 25, yPos);
    yPos += lines.length * 7;
  });
  
  // Page 5: Compatibility
  if (insights.compatibility) {
    doc.addPage();
    doc.setFillColor(255, 255, 255);
    doc.rect(0, 0, 210, 297, 'F');
    
    doc.setFontSize(20);
    doc.text('Best Compatibility Matches', 20, 30);
    
    yPos = 45;
    doc.setFontSize(11);
    
    insights.compatibility.best_matches.forEach((match) => {
      const compat = insights.compatibility.compatibility[match];
      
      doc.setFontSize(14);
      doc.text(`${match} (${compat.score}% Match)`, 20, yPos);
      yPos += 10;
      
      doc.setFontSize(10);
      const whyLines = doc.splitTextToSize(compat.why, 170);
      doc.text(whyLines, 20, yPos);
      yPos += whyLines.length * 6 + 5;
      
      doc.setFont(undefined, 'bold');
      doc.text('Challenge:', 20, yPos);
      doc.setFont(undefined, 'normal');
      const challengeLines = doc.splitTextToSize(compat.challenges, 160);
      doc.text(challengeLines, 42, yPos);
      yPos += challengeLines.length * 6 + 15;
      
      if (yPos > 270) {
        doc.addPage();
        yPos = 30;
      }
    });
  }
  
  // Page 6: Growth Tips
  doc.addPage();
  doc.setFillColor(255, 255, 255);
  doc.rect(0, 0, 210, 297, 'F');
  
  doc.setFontSize(20);
  doc.text('Personal Growth Tips', 20, 30);
  
  yPos = 45;
  doc.setFontSize(11);
  insights.growth_tips.forEach((tip, idx) => {
    const lines = doc.splitTextToSize(`${idx + 1}. ${tip}`, 170);
    doc.text(lines, 20, yPos);
    yPos += lines.length * 7 + 5;
  });
  
  yPos += 15;
  doc.setFontSize(20);
  doc.text('Famous People', 20, yPos);
  yPos += 15;
  
  doc.setFontSize(11);
  doc.text(insights.famous_people.join(', '), 20, yPos, { maxWidth: 170 });
  
  // Footer on last page
  doc.setFontSize(10);
  doc.setTextColor(100, 100, 100);
  doc.text('Generated by MindMorph - Personality Assessment Platform', 105, 285, { align: 'center' });
  
  // Save PDF
  doc.save(`MindMorph-${mbti}-Report.pdf`);
};