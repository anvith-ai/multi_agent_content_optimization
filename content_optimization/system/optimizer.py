# content_optimization/system/optimizer.py
from content_optimization.agents.generator import ContentGeneratorAgent
from content_optimization.agents.evaluator import ContentEvaluatorAgent
from typing import Dict, Tuple, List
import time
from difflib import unified_diff
from content_optimization.utils.config import Config

class ContentOptimizationSystem:
    def __init__(
        self, 
        api_key: str, 
        passing_grade: float = 80.0, 
        max_iterations: int = 3        
    ):
        self.generator = ContentGeneratorAgent(api_key)
        self.evaluator = ContentEvaluatorAgent(api_key)
        self.passing_grade = passing_grade
        self.max_iterations = max_iterations
        self.iteration_history = []

    def _parse_evaluation(self, evaluation: str) -> Tuple[float, Dict[str, float], str]:
        """
        Parse the evaluation response into structured components.
        Returns: (overall_grade, criterion_scores, feedback)
        """
        lines = evaluation.split('\n')
        criterion_scores = {}
        feedback_lines = []
        overall_grade = 0
        
        in_feedback = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if ':' in line and 'score' in line.lower():
                try:
                    criterion = line.split(':')[0].strip()
                    score = float(line.split(':')[1].split('/')[0].strip())
                    criterion_scores[criterion] = score
                except:
                    continue
                    
            elif 'overall grade' in line.lower():
                try:
                    overall_grade = float(line.split(':')[1].split('/')[0].strip())
                except:
                    continue
                    
            elif 'feedback' in line.lower():
                in_feedback = True
            elif in_feedback and line and not any(x in line.lower() for x in ['score', 'grade']):
                feedback_lines.append(line)
        
        feedback = '\n'.join(feedback_lines).strip()
        return overall_grade, criterion_scores, feedback

    def _print_content_comparison(self, old_content: str, new_content: str, iteration: int):
        """
        Print a comparison between old and new content versions.
        """
        if old_content:
            print("\nContent Changes:")
            # Split content into lines for comparison
            old_lines = old_content.split('\n')
            new_lines = new_content.split('\n')
            
            # Generate diff
            diff = list(unified_diff(
                old_lines,
                new_lines,
                fromfile=f'Iteration {iteration-1}',
                tofile=f'Iteration {iteration}',
                lineterm='',
            ))
            
            if diff:
                for line in diff:
                    if line.startswith('+') and not line.startswith('+++'):
                        print(f"\033[92m{line}\033[0m")  # Green for additions
                    elif line.startswith('-') and not line.startswith('---'):
                        print(f"\033[91m{line}\033[0m")  # Red for deletions
                    else:
                        print(line)
            else:
                print("No significant changes in content")
        
    def _format_content_block(self, content: str) -> str:
        """
        Format content block for display
        """
        separator = "-" * 80
        return f"\n{separator}\n{content}\n{separator}"
        
    def optimize_content(
        self, 
        prompt: str, 
        criteria: Dict[str, float]
    ) -> Tuple[str, float, str, int]:
        """
        Generate and optimize content until it passes the grade or reaches max iterations.
        """
        content = ""
        grade = 0
        feedback = ""
        iterations = 0
        previous_content = ""
        
        print("\n=== Starting Content Optimization Process ===")
        print(f"Target Grade: {self.passing_grade}")
        print(f"Maximum Iterations: {self.max_iterations}")
        print(f"\nPrompt: {prompt}\n")
        
        while grade < self.passing_grade and iterations < self.max_iterations:
            iterations += 1
            print(f"\n{'='*20} Iteration {iterations} {'='*20}")
            
            # Generate content
            print("\nGenerating content...")
            previous_content = content
            content = self.generator.generate_content(
                prompt=prompt, 
                previous_feedback=feedback
            )
            
            # Show current content
            print("\nGenerated Content:", self._format_content_block(content))
            
            # Show content changes if not first iteration
            if iterations > 1:
                self._print_content_comparison(previous_content, content, iterations)
            
            # Evaluate content
            print("\nEvaluating content...")
            evaluation_result = self.evaluator.evaluate_content(content, criteria)
            grade, criterion_scores, feedback = self._parse_evaluation(evaluation_result[1])
            
            # Store iteration results
            self.iteration_history.append({
                'iteration': iterations,
                'content': content,
                'grade': grade,
                'criterion_scores': criterion_scores,
                'feedback': feedback
            })
            
            # Print iteration results
            print("\nEvaluation Results:")
            print(f"Overall Grade: {grade:.1f}/100")
        #    print("\nCriterion Scores:")
        #    for criterion, score in criterion_scores.items():
        #        print(f"- {criterion}: {score:.1f}/100")

        #    if feedback:
        #        print("\nFeedback for Improvement:")
        #        print(feedback)
            
            # Add delay to respect API rate limits
            time.sleep(1)
        
        print("\n=== Optimization Process Complete ===")
        print(f"Final Grade: {grade:.1f}/100")
        print(f"Total Iterations: {iterations}")
        print(f"{'✓ Passed' if grade >= self.passing_grade else '✗ Did Not Pass'} (Target: {self.passing_grade})")
        
        # Print optimization summary
        self._print_optimization_summary()
        
        return content, grade, feedback, iterations
    
    def _print_optimization_summary(self):
        """
        Print a summary of the optimization process
        """
        print("\n=== Optimization History ===")
        for entry in self.iteration_history:
            print(f"\nIteration {entry['iteration']}:")
            print(f"Grade: {entry['grade']:.1f}/100")
        #    print("Criterion Scores:")
        #    for criterion, score in entry['criterion_scores'].items():
        #        print(f"- {criterion}: {score:.1f}/100")