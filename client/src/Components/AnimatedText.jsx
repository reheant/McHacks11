import React from 'react';


const AnimatedText = ({ text, animationClassName }) => {
  // Split the text into letters
  const letters = text.split('');

  return (
    <div>
      {letters.map((letter, index) => (
        <span
          key={index}
          className={animationClassName}
          style={{ animationDelay: `${index * 0.05}s`, display: 'inline-block', whiteSpace: 'pre' }}
        >
          {letter === ' ' ? '\u00A0' : letter}
        </span>
      ))}
    </div>
  );
};

export default AnimatedText;
