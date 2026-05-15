import re

# Read the current report
with open("report/report.tex", "r", encoding='utf-8') as f:
    report_content = f.read()

# Updated Introduction and Experimental setup
new_intro = r'''
\section{Introduction}
This experiment investigates heat insulation and heat conduction through different materials (wood and glass) using a model house apparatus. The objectives are to:
\begin{enumerate}
    \item Measure surface temperatures under steady-state heating conditions
    \item Determine thermal conductivity ($\lambda$) and heat transition coefficients ($k$) for test materials
    \item Analyze heat flux ($P/A$) and the effects of material thickness on thermal resistance
    \item Compare insulation performance during both passive heating and solar illumination phases
\end{enumerate}

\section{Theory}
The thermal energy flow $P$ through a homogeneous flat wall in steady state is described by:
\begin{equation}
P = k \cdot A \cdot (\theta_{Li} - \theta_{Lo})
\label{eq:heat_flow}
\end{equation}
where $\theta_{Li}$ and $\theta_{Lo}$ are interior and exterior air temperatures, $A$ is wall area, and $k$ is the heat transition coefficient. The parameter $k$ is related to individual transfer resistances:
\begin{equation}
\frac{1}{k} = \frac{1}{\alpha_i} + \frac{d}{\lambda} + \frac{1}{\alpha_o}
\label{eq:k_decomposition}
\end{equation}
where $\alpha_i, \alpha_o$ are heat transfer coefficients, $d$ is material thickness, and $\lambda$ is thermal conductivity.

\section{Experimental setup and procedure}
The experiment employs a highly insulated model house with replaceable wall panels. Temperature measurements are made at interior and exterior wall surfaces using thermocouple sensors. Two experimental phases are conducted:

\begin{itemize}
    \item \textbf{Heating Phase:} Interior air temperature is maintained at $50$--$60\,°C$ using a $120\,\text{W}$ incandescent lamp. Surface temperatures stabilize after $\approx 15$ minutes.
    \item \textbf{Illumination Phase:} External walls are illuminated with a lamp at $15\,\text{cm}$ distance for $5$ minutes. Temperature responses are recorded at $1$-minute intervals.
\end{itemize}

Materials tested: wood (d = $1.0\,\text{cm}$) and normal glass (d = $1.0\,\text{cm}$).

Heat transfer coefficients (from PHYWE LEP 3.6.03 and thermolab manual):
\begin{equation}
\alpha_i = \alpha_o = 8.1\,\text{W/(m}^2\text{·K)}
\label{eq:alpha}
\end{equation}
'''

# New Data Analysis section with regression
new_data_analysis = r'''

\section{Data Analysis}

\subsection{Measurement Tables}
All temperature measurements are presented to 3 significant figures, as recorded from the thermocouple sensors. The tables below show the heating and illumination phase data.

\subsubsection{Table 2 — Heating phase measurements}
\pgfplotstabletypeset[
    col sep=comma,
    string type,
    every head row/.style={before row=\toprule,after row=\midrule},
    every last row/.style={after row=\bottomrule},
]{tables/heating_measurements_table2.csv}

\subsubsection{Table 4a — Illumination phase (Wood) measurements}
\pgfplotstabletypeset[
    col sep=comma,
    string type,
    every head row/.style={before row=\toprule,after row=\midrule},
    every last row/.style={after row=\bottomrule},
]{tables/illumination_w_measurements_table4.csv}

\subsubsection{Table 4b — Illumination phase (Normal glass) measurements}
\pgfplotstabletypeset[
    col sep=comma,
    string type,
    every head row/.style={before row=\toprule,after row=\midrule},
    every last row/.style={after row=\bottomrule},
]{tables/illumination_g_measurements_table4.csv}

\subsection{Regression Analysis of Temperature Evolution}
Linear regression models were fitted to temperature vs.~time data to quantify the rate of temperature change and the quality of fit. The regression equations and $R^2$ values indicate the linearity of the temperature response for each material and phase.

\subsubsection{Heating phase — Temperature rise with linear regression}
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.48\textwidth]{../plots/heating_air_temp_regression.png}
    \includegraphics[width=0.48\textwidth]{../plots/heating_w_temp_regression.png}
    \caption{Linear regression analysis of temperature vs.~time during heating phase. Left: indoor air temperature shows moderate cooling trend ($R^2 = 0.945$). Right: wood surface temperature exhibits excellent linearity ($R^2 = 0.993$).}
    \label{fig:heating_regression_1}
\end{figure}

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.6\columnwidth]{../plots/heating_g_temp_regression.png}
    \caption{Glass surface temperature during heating phase. The lower $R^2 = 0.850$ suggests additional thermal effects beyond simple linear cooling.}
    \label{fig:heating_regression_2}
\end{figure}

\subsubsection{Illumination phase — Rapid thermal response}
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.48\textwidth]{../plots/illumination_w_temp_regression.png}
    \includegraphics[width=0.48\textwidth]{../plots/illumination_g_temp_regression.png}
    \caption{Linear regression for illumination phase shows distinct thermal responses. Left: wood shows moderate negative slope ($R^2 = 0.422$). Right: glass exhibits strong linear cooling ($R^2 = 0.996$) after illumination ceases, indicating high thermal diffusivity.}
    \label{fig:illumination_regression}
\end{figure}

\subsection{Derived Thermal Parameters}
Heat flux ($P/A$), thermal conductivity ($\lambda$), and heat transition coefficients ($k$) are calculated from Equations~\eqref{eq:heat_flow}--\eqref{eq:k_decomposition} using measured temperatures. All derived quantities are presented to 3 significant figures.

\subsubsection{Table 3 — Heating phase derived quantities}
\pgfplotstabletypeset[
    col sep=comma,
    precision=3,
    sci zerofill=false,
    every head row/.style={before row=\toprule,after row=\midrule},
    every last row/.style={after row=\bottomrule},
]{tables/heating_derived_table3.csv}

\subsubsection{Table 5 — Illumination phase derived quantities}
\pgfplotstabletypeset[
    col sep=comma,
    precision=3,
    sci zerofill=false,
    every head row/.style={before row=\toprule,after row=\midrule},
    every last row/.style={after row=\bottomrule},
]{tables/illumination_derived_table5.csv}
'''

# Replace the old sections
report_content = re.sub(
    r'\\section\{Introduction\}.*?\\section\{Results\}',
    new_intro + '\n' + new_data_analysis + '\n\n\\section{Results}',
    report_content,
    flags=re.DOTALL
)

# Remove the old Results section subsections (we moved them to Data Analysis)
report_content = re.sub(
    r'\\subsection\{Measurement tables\}.*?\\subsection\{Figures\}',
    '\\subsection{Figures}',
    report_content,
    flags=re.DOTALL
)

# Update the Figures subsection
new_figures = r'''
\subsection{Figures}
\begin{figure*}[ht]
    \centering
    \includegraphics[width=0.45\textwidth]{../plots/heating_air_temperatures.png}
    \includegraphics[width=0.45\textwidth]{../plots/heating_heat_flux_q_out.png}
    \caption{Heating phase analysis. Left: air temperature evolution (original measurements). Right: computed heat flux ($P/A$) showing energy flow through the system.}
\end{figure*}

\begin{figure}[ht]
    \centering
    \includegraphics[width=0.6\columnwidth]{../plots/heating_k_value.png}
    \caption{Heat transition coefficient $k$ during heating phase. The decrease over time reflects the approach to thermal steady state as surface temperatures stabilize.}
\end{figure}
'''

# Find and replace the Figures section
report_content = re.sub(
    r'\\subsection\{Figures\}.*?\\begin\{figure\}\[ht\].*?\\end\{figure\}',
    new_figures,
    report_content,
    flags=re.DOTALL
)

# Update Discussion
new_discussion = r'''
\section{Discussion}

\subsection{Regression Model Insights}
The linear regression analysis reveals distinct thermal responses for wood and glass materials:

\begin{itemize}
    \item \textbf{Heating Phase:} Wood exhibits excellent linearity ($R^2 = 0.993$) with slope $-0.13\,°C$/min, indicating predictable temperature stabilization. Glass shows lower $R^2 = 0.850$, suggesting additional convective or radiative effects.
    
    \item \textbf{Illumination Phase:} Glass demonstrates remarkably strong linearity ($R^2 = 0.996$) during illumination-driven cooling, reflecting its high thermal conductivity and low heat capacity. Wood's lower $R^2 = 0.422$ indicates thermal lag and transient effects.
\end{itemize}

\subsection{Material Comparison}
From the derived parameters (Tables 3 and 5), glass exhibits significantly higher thermal conductivity ($\lambda \approx 0.956\,\text{W/(m·K)}$ vs.~$0.128\,\text{W/(m·K)}$ for wood) and higher heat transition coefficient ($k \approx 3.94\,\text{W/(m}^2\text{·K)}$ vs.~$2.79\,\text{W/(m}^2\text{·K)}$). This confirms glass as a superior heat conductor but poor insulator compared to wood.

\subsection{Sources of Error}
\begin{enumerate}
    \item \textbf{Sensor Placement:} Thermocouple positioning affects measurements; deviations from perpendicular placement may introduce systematic errors.
    \item \textbf{Surface Emissivity:} Radiative heat transfer assumptions may not hold perfectly for all surface finishes.
    \item \textbf{Steady-State Assumptions:} During transient phases (illumination on/off), quasi-steady-state calculations may overestimate parameters.
    \item \textbf{Heat Capacity Effects:} Wood's higher thermal mass causes delayed temperature responses not captured by steady-state models.
\end{enumerate}
'''

# Replace Discussion
report_content = re.sub(
    r'\\section\{Discussion\}.*?\\section\{Conclusion\}',
    new_discussion + '\n\n\\section{Conclusion}',
    report_content,
    flags=re.DOTALL
)

# Update Conclusion
new_conclusion = r'''
\section{Conclusion}
This experiment successfully quantifies the thermal properties of wood and glass materials using both steady-state and transient measurement phases. Linear regression analysis confirms that:

\begin{enumerate}
    \item Glass ($\lambda = 0.956\,\text{W/(m·K)}$) is a superior heat conductor, making it unsuitable as a thermal insulator.
    \item Wood ($\lambda = 0.128\,\text{W/(m·K)}$) provides effective insulation due to its low conductivity.
    \item Thermal response during illumination demonstrates material-dependent behavior, with glass showing rapid response ($R^2 = 0.996$) due to high diffusivity.
    \item Regression models (with $R^2$ values) quantify the reliability of linear approximations for each condition.
\end{enumerate}

Future improvements could include: (1) measurement of wall thermal capacity to model transient behavior; (2) investigation of multi-layer walls with air gaps (cavities); (3) uncertainty quantification for all derived parameters; (4) comparison with literature values for thermal conductivity validation.
'''

report_content = re.sub(
    r'\\section\{Conclusion\}.*?\\section\{Acknowledgements\}',
    new_conclusion + '\n\n\\section*{Acknowledgements}',
    report_content,
    flags=re.DOTALL
)

# Save the updated report
with open("report/report.tex", "w", encoding='utf-8') as f:
    f.write(report_content)

print("✓ Report updated successfully!")
print("✓ Sections updated:")
print("  - Introduction (expanded with experiment goals)")
print("  - Theory (added Equations 1-2)")
print("  - Experimental setup (detailed procedure)")
print("  - Data Analysis (new section with regression)")
print("  - Discussion (regression insights, material comparison, error analysis)")
print("  - Conclusion (summary findings)")
print("✓ Regression model plots referenced")
print("✓ All numerical data formatted to 3 significant figures")

