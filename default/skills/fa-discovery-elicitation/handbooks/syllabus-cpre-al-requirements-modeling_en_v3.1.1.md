3.1.1 | July, 30, 2024
Syllabus
Requirements Modeling
Practitioner | Specialist
Lars Baumann, Thosten Cziharz,
Colin Hood, Peter Hruscka,
Ursula Meseberg, Stefan Queins,
Artur Strasser, Thorsten Weyer





Requirements Modeling | Syllabus | © IREB
2 | 26
Terms of use
1. Individuals and training providers may use this syllabus as a basis for seminars,
provided that the copyright is acknowledged and included in the seminar materials.
Anyone using this syllabus in advertising needs the written consent of IREB for this
purpose.
2. Any individual or group of individuals may use this syllabus as basis for articles, books
or other derived publications provided the copyright of the authors and IREB e.V. as
the source and owner of this document is acknowledged in such publications.
© IREB e.V.
All rights reserved. No part of this publication may be reproduced, stored in a retrieval
system or transmitted in any form or by any means, electronic, mechanical, photocopying,
recording or otherwise, without either the prior written permission of the authors or IREB e.V.
Acknowledgements
This syllabus was produced by (in alphabetical order): Lars Baumann, Thorsten Cziharz, Colin
Hood, Peter Hruschka, Ursula Meseberg, Stefan Queins, Artur Strasser, and Thorsten Weyer.
Sincere thanks to all for their commitment, which was given voluntarily.
Copyright © 2024 of the syllabus IREB Certified Professional for Requirements Engineering,
Modul Requirements Modeling, is with the authors listed. Rights are transferred to the IREB
International Requirements Engineering Board e.V.
Foreword
This module is a basis for further education and training for requirements engineers,
business analysts, process and system analysts, and any other project participants who want
to model requirements in requirements engineering or who want to work with requirements
models. The aim of the module is to convey knowledge about how to model requirements
usefully and effectively in requirements engineering. Furthermore, the module explains how
requirements modeling can be used in practice (where applicable, in addition to textual
requirements) to do the following: to communicate requirements such that they are easier to
understand; to make the complexity of the requirements of a system more manageable;
and, through the high level of formalization of the requirements modeled, to enable a greater
degree of automation in system development activities (for example, quality assurance for
the requirements specification, derivation of system test cases).
Purpose of the document
This syllabus defines educational objectives and a summary of the educational content for
the Requirements Modeling Practitioner and Specialist established by the International
Requirements Engineering Board (IREB). The syllabus provides training providers with the
basis for creating their course materials. Students can use the syllabus to prepare
themselves for the examination.



Requirements Modeling | Syllabus | © IREB
3 | 26
Contents of the syllabus
The module Requirements Modeling addresses professionals with career profiles like
Requirements Engineering, business analysis, business engineering, and organizational design,
who wish to extend their knowledge and skills in the area of requirements modeling.
Content scope
This Parctitioner/Specialist level covers the topic "Model-based Specification of
Requirements" in more detail compared to the foundation level. The training focuses on
modeling requirements in relation to information structures, functions, and behavior. It also
covers scenario modeling in requirements engineering. Separate modules have already been
published for a more detailed study of the other educational units in the foundation level of
the Certified Professional for Requirements Engineering certificate (for example,
Requirements Elicitation, Requirements Management) and RE@Agile.
The following table gives an overview of the course content of the CPRE Modul
Requirements Modeling and the proposed duration of training for the different topic areas.


Topic
Content
Time
required
1
Basic principles of
requirements
modeling
Reasons for requirements modeling, forms of
requirements modeling, terms and concepts,
views, benefits of requirements modeling,
quality of requirements models
90 minutes
2
Context modeling
Purpose of context modeling, terms, basic
elements, data flow-oriented context
modeling, and further forms of context
modeling
120 minutes
3
Modeling
information structures
Purpose of information structure modeling in
requirements engineering; modeling classes,
attributes, and data types; modeling
associations; generalization and specialization
relationships; aggregation and composition
relationships; further modeling concepts
270 minutes
4
Modeling dynamic
views
Dynamic views in requirements modeling, use
case modeling, data flow-oriented and
control flow-oriented modeling, state-
oriented modeling
435 minutes



Requirements Modeling | Syllabus | © IREB
4 | 26

Topic
Content
Time
required
5
Modeling
scenarios
Purpose of scenario modeling, the
relationship between scenarios and use cases,
scenario modeling with sequence diagrams
and communication diagrams
165 minutes

Level of Detail
The level of detail of this syllabus allows internationally consistent teaching and examination.
To reach this goal, the syllabus contains the following:
▪
General educational objectives,
▪
Contents with a description of the educational objectives and
▪
References to further literature (where necessary).
The syllabus was developed based on the IREB Certified Professional for Requirements
Engineering Foundation Level and covers the modeling of requirements in the form of
diagrams. The Modul Requirements Modeling uses a more differentiated view concept
compared to the concept used in the foundation level. This more differentiated view allows
you to specify the requirements of very extensive and complex systems in a well-structured
and more formal way in order to cope with the large extend and complexity of the
requirements specification. In this module, requirements are modeled in the information
structure view, the data flow-oriented view, the control flow-oriented view, the state-
oriented view, and the scenario view using suitable types of diagrams. An important aspect
of this module is also to convey knowledge about the relationships between the different
views in requirements modeling. To achieve this objective, the module looks at the basic
principles from the foundation level in more detail, adding aspects that cover expert
knowledge and best practices.
Educational objectives / Cognitive knowledge levels
All modules and educational objectives in this syllabus are assigned a cognitive level. The
levels are classified as follows:
▪
L1: Know (describe, enumerate, characterize, recognize, name, remember, ...) — The
candidate can remember or retrieve previously learned material.
▪
L2: Understand (explain, interpret, complete, summarize, justify, classify, compare, ...)
— The candidate can grasp/construct meaning from given material or situations.
▪
L3: Apply (specify, write, design, develop, implement, ...) — The candidate can apply
knowledge and skills in given situations.
▪
L4: Analyze (investigate, conclude from, provide arguments for, ...) — The candidate
can analyze a given problem, argue what should/can be done, break down the
problem into parts, apply critical thinking, argue about causes and effects.



Requirements Modeling | Syllabus | © IREB
5 | 26
▪
L5: Evaluate (critique, judge) — The candidate can give a well-argued critique of a
given artifact; make a profound judgment in a given case. Note that an educational
objective at cognitive knowledge level Ln also contains elements of all lower cognitive
knowledge levels (L1 through Ln-1).
Note that an educational objective at cognitive knowledge level Ln also contains elements of
all lower cognitive knowledge levels (L1 through Ln-1).
Example:
An educational objective of the type “Apply the RE technique xyz” is at the cognitive knowledge
level (L3). However, the ability to apply requires that students first know the RE technique xyz
(L1) and that they understand what the technique is used for (L2).
!
All terms used in this syllabus and defined in the IREB Glossary have to be
known (L1), even if they are not explicitly mentioned in the educational
objectives.
The glossary is available for download on the IREB homepage at
https://www.ireb.org/en/downloads/#cpre-glossary-2-0
This syllabus and the related handbook use the abbreviation “RE” for Requirements
Engineering.
Structure of the syllabus
The syllabus consists of five main chapters. Each chapter covers one educational unit (EU).
Main chapter titles contain the cognitive level of their chapters, which is the highest level of
their sub-chapters. Furthermore, the teaching time is suggested that is the minimum a
course should invest for that chapter. Training companies are free to devote more time to
the EUs and the exercises, but make sure that the proportions between the EUs are
maintained. Important terms within the chapter are listed at the beginning of the chapter.





Requirements Modeling | Syllabus | © IREB
6 | 26
Example:
Chapter 1:
Basic Principles of Requirements Modeling (L1)
Duration:
120 minutes
Terms:
Model, graphical model, view, requirements view, requirements model, modeling
constructs, model element, modeling language
The example shows that Chapter 1 contains educational objectives at level L1 and 120
minutes are intended for teaching the material in this chapter.
Each chapter contain subchapters. Their titles also contain the cognitive level of their
content.
The educational objectives are listed before the actual text. The numbering shows to which
sub-chapter they belong.

Example:
EO 3.1.2
This example shows that  educational objective EO 3.1.2 is described in sub-chapter 3.1.
The examination
This syllabus covers educational units and educational objectives for the certification exams
of the
▪
Requirements Modeling Practitioner
▪
Requirements Modeling Specialist
The exam to achieve the Requirements Modeling Practitioner certificate consists of a
multiple-choice exam.
The exam to achieve the Requirements Modeling Practitioner certificate consists of a
multiple-choice exam.
The exam to achieve the Requirements Modeling Specialist certificate consists of a written
assignment.
Both exams include exam questions covering all educational units and all educational
objectives in the syllabus.
Each exam question may include material from multiple chapters of the syllabus as well as
from multiple educational objectives or portions of an educational objective.
The multiple-choice exam for the Practitioner certificate
▪
tests all educational objectives of the syllabus. However, for the educational
objectives at cognitive knowledge levels L4 and L5, the exam questions are limited to
items at cognitive levels L1 through L3.
▪
can be taken immediately following a course, but also independently of that (e.g.,
remotely or at a test center).



Requirements Modeling | Syllabus | © IREB
7 | 26
The written assignment for the Specialist certificate
▪
tests all educational objectives of the syllabus at the cognitive knowledge levels
indicated for each educational objective.
▪
follows the task description for Requirements Modeling - Specialist -, found at
https://www.ireb.org/en/downloads/tag:advanced-level-written-assignment#top.
▪
is self-paced and submitted to a licensed Certification Body.
The following generic educational objectives also apply to the written assignment for the
Specialist certificate:
EO G1:
Analyze and illustrate Requirements Modeling problems in a context that the can-
didate is familiar with, or which is similar to such a context (L4).
EO G2:
Evaluate and reflect on the usage of Requirements Modeling practices, methods,
processes, and tools in projects in which the candidate was involved (L5).
A list of IREB licensed certification bodies can be found on the website https://www.ireb.org.





Requirements Modeling | Syllabus | © IREB
8 | 26
Version History
Version
Date
Comment
2.0.0
September 9, 2015
Initial version
2.1.0
July 11, 2016
Corrections of the effort distribution
2.2.0
August 31, 2016
Topic “Association classes” added to EU 3.3
3.0.0
July 1, 2022
Information about Advanced Level exam split added.
Switched to new cognitive Levels of knowledge (5
levels). Educational objectives modified accordingly.
3.1.0
May 24, 2024
New Corporate Design implemented,
Cognitive Knowledge Levels synchronized,
Term “Advanced Level removed”
3.1.1
July 30, 2024
References to Requirements Eliciation removed in the
introduction





Requirements Modeling | Syllabus | © IREB
9 | 26
Table of Contents
1 Basic principles of requirements modeling (L1) .......... 11
1.1
Motivation for requirements modeling and fundamentals (L1) ........ 11
1.2
Overview of the views and languages of requirements modeling (L1) . 12
1.3
Adapting modeling languages and integrating textual requirements (L1)
 .................................................................. 12
1.4
The benefits of requirements modeling and the quality of requirements
models (L1) ....................................................... 12
2 Context modeling in requirements engineering (L3) ....... 13
2.1
The purpose of context modeling and conceptual fundamentals (L1) .. 13
2.2
Basic elements of context modeling (L3) ........................... 14
2.3
Notation and rules for context modeling with data flow diagrams (L3)
 .................................................................. 14
2.4
Other types of context modeling (L2) .............................. 14
3 The information structure view in requirements modeling
(L3) .................................................... 15
3.1
The purpose of information structure modeling (L1) ................ 16
3.2
Modeling classes, attributes, and data types (L3) ................. 16
3.3
Modeling simple relationships, aggregations, and compositions (L3) 16
3.4
Modeling generalization and specialization (L3) ................... 17
3.5
Further modeling concepts (L1) .................................... 17
4 Dynamic views in requirements modeling (L4) ............. 18
4.1
Overview of the dynamic views of requirements modeling (L1) ....... 19
4.2
The purpose and modeling constructs of use case modeling (L2) ..... 19
4.3
Identifying use cases and specifying them in text form (L3) ....... 20



Requirements Modeling | Syllabus | © IREB
10 | 26
4.4
Structuring use cases and packages (L3) ........................... 20
4.5
Data flow modeling, control flow modeling, and diagram types (L2) . 20
4.6
Requirements modeling with data flow diagrams (L3) ................ 21
4.7
Requirements modeling with activity diagrams (L3) ................. 21
4.8
Combining and decomposing functions, and ensuring consistency (L4) 21
4.9
The purpose of state-oriented modeling and modeling constructs (L1) 22
4.10 Requirements modeling with state machines (L3) .................... 22
5 Scenario modeling in requirements engineering (L3) ...... 23
5.1
Basic principles of scenario modeling in requirements engineering
(L3) .............................................................. 24
5.2
Simple scenario modeling with sequence diagrams (L3) .............. 24
5.3
Advanced scenario modeling with sequence diagrams (L3) ............ 25
5.4
Scenario modeling with communication diagrams (L3) ................ 25




Requirements Modeling | Syllabus | © IREB
11 | 26
1 Basic principles of requirements modeling
(L1)
Duration: 90 minutes (theory)
Terms:
Model, graphical model, view, requirements view, requirements model, modeling
constructs, model element, modeling language
Educational objectives
EO 1.1
Know the motivation for modeling requirements, as well as applications and basic
terms of requirements modeling
EO 1.2
Know the views and related languages of requirements modeling at a general
level
EO 1.3
Know the possibilities for adapting modeling languages and integrating textual
and modeled requirements
EO 1.4
Know the benefits of requirements modeling as well as quality criteria for require-
ments models
Prerequisite: Basic knowledge of conceptual modeling, basic views in requirements
modeling (foundation level), understanding of simple requirements diagrams
Topic overview: This educational unit looks at the basic principles of requirements modeling.
It covers the reasons why requirements are (also) modeled, as well as the various fields of
use and the main terms for requirements modeling. Furthermore, this unit introduces the
more differentiated views used in requirements modeling compared to the CPRE foundation
level and looks at the link between textual requirements and modeled requirements. The unit
also discusses the benefits of requirements modeling and introduces the general criteria for
assessing the quality of requirements models.
Literature reference: Chapter 1, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-requirements-
modeling
1.1 Motivation for requirements modeling and fundamentals (L1)
Duration: 30 minutes (theory)
Content: In this educational unit you become familiar with the difference between textual
and modeled requirements and learn about the different benefits of modeling requirements.
You learn that you can use requirements models to make the scope and complexity of
requirements more manageable, for example, and that modeling requirements makes it
easier to specify and communicate requirements clearly to prevent misunderstandings. You
also learn the different applications of requirements modeling (e.g., for the precise and
unique specification of requirements or for structuring and visualizing complex
circumstances), as well as the main terms and concepts of requirements modeling (e.g.,
requirements model, notation element, model element, modeling language).



Requirements Modeling | Syllabus | © IREB
12 | 26
1.2 Overview of the views and languages of requirements
modeling (L1)
Duration: 15 minutes (theory)
Content: In this educational unit you become familiar with the more differentiated view
concept used in requirements modeling compared to the CPRE foundation level. At the
highest level, this concept differentiates between the context view, the information
structure view, and the dynamic view. The dynamic view in turn looks at the behavior of the
system from various viewpoints. It also differentiates between the use case view, the data
flow-oriented view, and the control flow-oriented view (also referred to as the process-
oriented view), as well as the scenario view and the state-oriented view. This unit gives you a
general overview of the relationships between the individual views and the languages
suitable for modeling the different views in requirements modeling.
1.3 Adapting modeling languages and integrating textual
requirements (L1)
Duration: 15 minutes (theory)
Content: In this educational unit you become familiar with the different options for adapting
modeling languages for requirements modeling, for example to increase the informative
value of the requirements models created and to adapt the modeling languages to the
demands of specific application areas (e.g., the development of information systems versus
embedded systems; the development of systems in the banking and insurance area versus
the development of systems for the automotive segment or for automated systems).
Furthermore, this unit gives you a general overview of how you can combine textual
requirements with modeled requirements. It explains which relationships can be used to
place model elements (graphical and/or textual) in relation to one another in the
requirements model.
1.4 The benefits of requirements modeling and the quality of
requirements models (L1)
Duration: 30 minutes (theory)
Content: In this educational unit you become familiar with the various benefits of modeling
requirements compared to documenting them in text form. These benefits include the
inherent support for the principle of "divide and conquer", the lower risk of ambiguity, and
the improved options for processing modeled requirements automatically. Furthermore, you
become familiar with the three quality criteria for requirements models: syntactic, semantic,
and pragmatic quality. You can use these criteria to assess and improve the quality of
requirements models in a systematic way.



Requirements Modeling | Syllabus | © IREB
13 | 26
2 Context modeling in requirements
engineering (L3)
Duration: 60 minutes (theory); 60 minutes (exercises)
Terms:
System boundary, context boundary, context diagram
Educational objectives
EO 2.1
Know the purpose of context modeling in requirements engineering
EO 2.2
Apply the basic elements of context modeling
EO 2.3
Master and use the notation and rules for context modeling with data flow dia-
grams
EO 2.4
Master and use other types of context modeling and their specific properties
Prerequisite: Basic knowledge of the importance of the system boundaries and the system
context for requirements engineering (CPRE foundation level), understanding of simple
requirements diagrams and in particular, use case diagrams
Topic overview: This educational unit establishes the importance of context modeling for
requirements engineering. It explains the knowledge that has to be obtained about the
context of a system under consideration and how you can document the context view
effectively. The unit introduces the basic elements of a data flow-oriented context modeling
for documenting the operational context of a system under consideration. In addition to
discussing notation elements for context modeling with data flow diagrams, the unit also
looks at pragmatic rules for using data flow diagrams for context modeling. The unit gives an
outlook with regard to other forms of context modeling in the use case view and the scenario
view.
Literature reference: Chapter 2 and Section 4.2.3, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-requirements-
modeling
2.1 The purpose of context modeling and conceptual
fundamentals (L1)
Duration: 15 minutes (theory)
Content: In this educational unit you refresh your knowledge of the terms system boundary
and context boundary (CPRE foundation level). You deepen your understanding of the
purpose of the context view and the importance of the context for system requirements.
You learn what knowledge about the operational context of a system should be
documented, how the context view differs from the other views in requirements modeling,
and the value this view has for the work of a requirements engineer.





Requirements Modeling | Syllabus | © IREB
14 | 26
2.2 Basic elements of context modeling (L3)
Duration: 15 minutes (theory)
Content: In this educational unit you become familiar with the basic elements of context
modeling and learn about the focus of data flow-oriented context modeling. Examples help
you become familiar with the results of data flow-oriented context modeling in various forms
of notation and the unit discusses the properties of the diagrams used for context modeling.
2.3 Notation and rules for context modeling with data flow
diagrams (L3)
Duration: 15 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you become familiar with possible modeling constructs for
data flow-oriented context modeling based on the data flow diagrams of the Structured
Analysis method according to DeMarco. You learn how these modeling constructs are used
to represent a system in its context. Furthermore, you learn simple and pragmatic rules that
you can use to check the completeness, the clarity, and the correct understanding of the
knowledge modeled via the system context.
2.4 Other types of context modeling (L2)
Duration: 15 minutes (theory); 30 minutes (exercises)
Content: It is not only data flow-oriented context modeling that focuses on the interfaces of
a system to its neighboring systems or human users; the cooperation of a system with the
neighboring systems or human users in its context is also a topic for the use case view and
the scenario view. In this educational unit you gain some first insights into context modeling
with use case diagrams and scenarios. Via examples, you learn the difference between
context modeling with use case diagrams or scenarios, and data flow-oriented context
modeling. The topic in this educational unit is covered in more detail in educational units EU 4
and EU 5.



Requirements Modeling | Syllabus | © IREB
15 | 26
3 The information structure view in
requirements modeling (L3)
Duration: 120 minutes (theory); 150 minutes (exercises)
Terms:
Information structure, UML class diagram, class, attribute, data type, binary as-
sociation, aggregation, composition, generalization, specialization
Educational objectives
EO 3.1
Know the purpose and importance of information structure modeling
EO 3.2.1
Master and use the syntax and semantics of the elements class, attribute, and
data type in UML class diagrams for modeling information structures
EO 3.2.2
Master and use heuristics for determining classes, attributes, and data types
EO 3.3.1
Master and use the syntax and semantics of simple relationships (binary associa-
tions) as well as aggregations and compositions
EO 3.3.2
Master and use heuristics for determining simple relationships
EO 3.3.3
Master and use heuristics for determining aggregations
EO 3.3.4
Master and use practical tips for modeling relationships
EO 3.4.1
Master and use the syntax and semantics of generalizations
EO 3.4.2
Master and use heuristics for determining generalizations
EO 3.4.3
Master and use practical tips for modeling generalizations
EO 3.5
Know further modeling concepts
Prerequisite: Basic knowledge of requirements modeling in the structure perspective (CPRE
foundation level), understanding of simple UML class diagrams
Topic overview: In requirements engineering, it is vitally important to understand and specify
the specific terms and data of an application domain. The diagrams of the information
structure view allow you to document relationships and properties of the terms beyond the
textual definitions of a glossary and thus create a deeper understanding of the application
domain. The diagrams are also suitable for specifying requirements that relate to the
structure of information and data. The aim of this educational unit is to build up the
theoretical and practical knowledge necessary for developing stable information structure
models. It introduces the UML class diagrams for modeling. The unit looks at the syntax and
semantics of the elements and relationships that appear in class diagrams and goes into
more detail about how to create class diagrams. It focuses in particular on describing
heuristics that make it easier to start modeling information structures, as well as on
recommendations and tips from practice.
Literature reference: Chapter 3, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-requirements-
modeling




Requirements Modeling | Syllabus | © IREB
16 | 26
3.1 The purpose of information structure modeling (L1)
Duration: 15 minutes (theory)
Content: In this educational unit you learn why information structure modeling is so
important within requirements modeling. The unit demonstrates which additional knowledge
about specific terms and data you can document in the information model compared to a
purely textual glossary. Furthermore, you learn how modeling the information structure
contributes to specifying requirements. The unit introduces UML class diagrams as a means
of expression for modeling information structures. You learn about the opportunities these
diagrams provide for the requirements engineers when specifying the requirements for a
system.
3.2 Modeling classes, attributes, and data types (L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: This educational unit introduces the central elements of information structure
models based on UML class diagrams: class, attribute, data type. You learn the difference
between classes and objects as well as the syntax and semantics of classes. To enable you
to begin modeling information structures, you learn how to derive the classes, attributes, and
data types from the terms known in the application domain. This educational unit offers you
different heuristics for this purpose. You learn how to specify classes more precisely using
attributes and how to differentiate classes from attributes. You also become familiar with
the syntax and semantics of attributes, as well as heuristics for identifying attributes. The
unit introduces three forms of attributes types. It also explains the syntax and semantics of
these form of attribute types and presents heuristics for modelling them in a correct way.
Furthermore, the unit provides tips for modeling classes, attributes, and data types in
practice.
3.3 Modeling simple relationships, aggregations, and
compositions (L3)
Duration: 30 minutes (theory); 60 minutes (exercises)
Content: It is not only classes that contain important information about the application
domain; the relationships that connect the objects of classes also contain important
information. This educational unit presents the most common types of relationships in
requirements modeling: simple relationships (binary associations), aggregations, and
compositions as well as the modeling of attributes of relationships by using association
classes. You become familiar with the syntax and semantics of these three types of
relationship according to UML.
The unit provides you with heuristics for determining simple relationships, aggregations, and
compositions. Furthermore, for modeling in practice, the unit also gives recommendations
on topics such as navigability versus reading direction and interpretation of multiplicities.



Requirements Modeling | Syllabus | © IREB
17 | 26
3.4 Modeling generalization and specialization (L3)
Duration: 15 minutes (theory); 60 minutes (exercises)
Content: Modeling generalization relationships allows you to further structure an information
model and to cope with complexity by abstracting from commonalities of different classes.
In this educational unit you learn the syntax and semantics of generalizations. The unit
introduces the concept of the abstract class. You learn how to use generalization sets and
become familiar with their typical constraints. The unit provides heuristics for determining
generalizations. It also gives practical recommendations for modeling generalizations.
3.5 Further modeling concepts (L1)
Duration: 30 minutes (theory)
Content: Information models in requirements engineering often contain similar specialized
facts and there are solutions in the form of patterns for modeling these facts. This
educational unit focuses on providing an overview of the most important analysis patterns
for information models as a further modeling concept. It also gives various structuring tips
for creating information structure models of high quality.



Requirements Modeling | Syllabus | © IREB
18 | 26
4 Dynamic views in requirements modeling
(L4)
Duration: 255 minutes (theory); 180 minutes (exercises)
Terms:
Dynamic view, use case, use case diagram, use case model, data flow, control
flow, object flow, data flow diagram, use case specification, activity diagram,
function, activity, action, state, state machine, event, hierarchization, concur-
rency
Educational objectives
EO 4.1
Know the dynamic views in requirements modeling
EO 4.2
Know the purpose and modeling constructs of use case diagrams
EO 4.3
Master the finding and specification of use cases
EO 4.4
Master the structuring and packaging of use cases
EO 4.5
Understand the purpose of data flow modeling and control flow modeling as well
as related diagram types and modeling constructs
EO 4.6
Master requirements modeling with data flow diagrams and relationships to use
case modeling, control flow modeling, and information structure modeling
EO 4.7
Master requirements modeling with activity diagrams and relationships to use
case modeling and scenario modeling
EO 4.8
Analyze the combination, decomposition, and specification of functions and as-
sessment of the consistency between different levels of abstraction
EO 4.9
Know the purpose of state-oriented modeling of requirements and modeling
constructs of state machines
EO 4.10
Master requirements modeling with state machines
Prerequisite: Knowledge of the functional and behavioral views in requirements modeling
(foundation level); the ability to read use case diagrams, simple data flow diagrams, simple
activity diagrams, and simple state machines
Literature reference: Chapter 4, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-requirements-
modeling
Topic overview: A significant proportion of the requirements for a system relates to the
behavior required of the system to allow it to fulfill its purpose during operation. Typically,
today's systems must have a very complex behavior toward their environment to be able to
fulfill the intended purpose during operation. This behavior has to be understood and
specified from various perspectives and at various levels of detail in order to make the
complexity of the required system behavior toward the environment manageable in
requirements engineering. The aim of this educational unit is to build up the theoretical and
practical knowledge required for specifying the requirements of the behavior of systems in
the form of requirements models. It introduces use case modeling to enable a general
modeling of the user-related functions of the system under consideration. To enable you to
model detailed requirements, the unit looks at function modeling in the form of data flow
diagrams and UML activity diagrams. Special attention is given to the differentiation
between data flow modeling and control flow modeling. One focus of this educational unit is
on describing heuristics for function modeling with data flow diagrams and activity diagrams
in order to create meaningful, high-quality requirements models. In addition to use case



Requirements Modeling | Syllabus | © IREB
19 | 26
modeling and function modeling, the unit also covers state-oriented requirements modeling
using the modeling of UML statecharts and state machine diagrams.
For all diagram types considered, the unit looks at the syntax and semantics of the different
modeling constructs and uses exercises to demonstrate the creation of diagrams of the
various types in more detail. The unit covers the integration of diagrams of different types in
the dynamic view of requirements modeling and the relationship to the information structure
view. It focuses in particular on describing heuristics that make it easier for you to start
modeling dynamic views in requirements modeling, as well as on recommendations and tips
from practice.
4.1 Overview of the dynamic views of requirements modeling
(L1)
Duration: 15 minutes (theory)
Content: This educational unit provides an overview of the different dynamic views of
requirements modeling. In requirements modeling, the dynamic views contain requirements
for the required behavior of the system under consideration. In order to make complex
system behavior manageable in the requirements, in the dynamic views the following
different views for modeling requirements are differentiated: use case view, data flow-
oriented view, control flow-oriented view, and the state-oriented view and scenarios. This
educational unit characterizes each of these views and demonstrates the relationships
between the different dynamic views. It also looks at the general relationships of dynamic
views to the information structure view.
4.2 The purpose and modeling constructs of use case modeling
(L2)
Duration: 15 minutes (theory)
Content: In this educational unit you become familiar with the purpose of use case modeling
in requirements engineering and refresh the knowledge you gained about use case diagrams
in the CPRE foundation level. For this purpose, the unit looks at the syntax and semantics of
the basic modeling constructs of use case diagrams, such as system boundary, actor, use
case, and association.





Requirements Modeling | Syllabus | © IREB
20 | 26
4.3 Identifying use cases and specifying them in text form
(L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: This educational unit provides practical help to support you in identifying use cases
and determining the correct level of granularity or functional scope for use cases in
requirements modeling. You learn how to identify use cases for a system under
consideration by deriving them systematically from the identification of events.
Furthermore, you learn how to specify individual use cases in detail using structured text
based on templates. In use case diagrams, use cases are presented in relation to actors in
the system context and, if applicable, to other use cases. This unit also contains exercises for
two areas: identifying use cases by identifying events in context or time-based events, and
specifying use cases in text form based on a use case template.
4.4 Structuring use cases and packages (L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you learn how to structure use cases effectively by explicitly
modeling relationships between uses cases within use case diagrams. To refresh the
knowledge gained from the CPRE foundation level, the unit first looks at the syntax and
semantics of the different relationships that can exist between use cases. You learn how to
model include and extend relationships between use cases. Furthermore, you learn how to
model generalization relationships for use cases. Similarly to modeling generalization
relationships between classes in the information structure view, this enables you to also
model generalized use cases and, based on these, specialized use cases. Finally, the unit
looks at packaging use cases, which enables you, for example, to regard the user-related
functions at various levels of granularity using use case diagrams.
4.5 Data flow modeling, control flow modeling, and diagram
types (L2)
Duration: 15 minutes (theory)
Content: This educational unit covers the purpose of data flow modeling and control flow
modeling. In particular, it addresses the difference between modeling data flows and
modeling control flows. To refresh the knowledge gained from the CPRE foundation level,
the unit also covers the syntax and semantics of the elementary modeling constructs of
data flow modeling (processes) and control flow modeling (activities, actions).





Requirements Modeling | Syllabus | © IREB
21 | 26
4.6 Requirements modeling with data flow diagrams (L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you become familiar with requirements modeling in the data
flow-oriented view using data flow diagrams. The unit looks at the syntax and semantics of
the different modeling constructs of data flow diagrams and offers tips for good data flow
diagrams. These tips cover, for example, using meaningful (expressive) designations for
processes, data flows, and data stores, as well as sources and sinks in the system context.
Finally, the unit addresses the relationships between modeling data flows and modeling use
cases, control flows, and information structures.
4.7 Requirements modeling with activity diagrams (L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you learn about requirements modeling in the control flow-
oriented view using activity diagrams. You become familiar with the syntax and semantics of
different modeling constructs of activity diagrams as well as rules and tips for requirements
modeling with activity diagrams. The unit also covers the modeling of object flows and data
flows with the aid of pins. Furthermore, it demonstrates the relationships between activity
diagrams and use case and scenario modeling. The unit focuses in particular on the common
modeling of the control flow of use cases, i.e., the main, alternative, and exception scenarios
within an activity diagram. It also covers the modeling of interruptible activity regions as well
as the sending and receiving of signals.
4.8 Combining and decomposing functions, and ensuring
consistency (L4)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you learn how to combine and decompose functions (i.e.,
processes or activities and actions) in data flow diagrams and activity diagrams, allowing
you to manage the scope and complexity of the requirements in the data flow-oriented and
control flow-oriented views in requirements modeling. This enables you to define hierarchy
levels for requirements and thus, for example, to model requirements for different
stakeholders more abstractly and in more detail consistently at the respective appropriate
level of abstraction or detail. The unit also addresses the specification of functions in text
form. You also become familiar with simple rules for defining consistent hierarchies for data
flow diagrams (visible balancing as well as data dictionary balancing between hierarchy
levels). Example exercises allow you to practice combining and decomposing processes in
data flow diagrams as well as activities and actions in activity diagrams.





Requirements Modeling | Syllabus | © IREB
22 | 26
4.9 The purpose of state-oriented modeling and modeling
constructs (L1)
Duration: 15 minutes (theory)
Content: In this educational unit you become familiar with the purpose of state-oriented
modeling of requirements in requirements engineering and refresh the corresponding
knowledge you gained from the CPRE foundation level. For this purpose, the unit looks at the
syntax and semantics of the basic modeling constructs of state machines, such as state,
state transition, event, and condition. The unit also addresses the relationship to data flow
modeling and control flow modeling and to information structure models.
4.10
Requirements modeling with state machines (L3)
Duration: 45 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you learn about requirements modeling in the state-
oriented view using UML state machine diagrams. The unit looks at the syntax and semantics
of the various modeling constructs of state machine diagrams and provides rules and tips
on, for example, finding states and state transitions. You learn how to model entry, exit, and
do functions in the states of a state machine diagram and how to model deferred triggers
and functions in states. Furthermore, you learn how to model state transitions with events,
boolean conditions (guards), and functions (effects). The focus of this educational unit is on
modeling composite states and substate machines. For complex state-oriented behavior,
this allows you to abstract hierarchically from partial behavior and thus manage the
complexity of the state-oriented behavior in the requirements. You learn how to model
histories (i.e., the memory of hierarchical state machines) and rules so that you can identify
composite states and substate machines and define effective and consistent hierarchies for
state machine diagrams. You learn how to model orthogonal regions in state-oriented
behavior and how to model synchronization point for orthogonal behavior.



Requirements Modeling | Syllabus | © IREB
23 | 26
5 Scenario modeling in requirements
engineering (L3)
Duration: 90 minutes (theory); 75 minutes (exercises)
Terms:
Model, graphical model, view, requirements view, requirements model, modeling
constructs, model element, modeling language
Educational objectives
EO 5.1
Master and use the purpose and different approaches for scenario modeling in
requirements engineering as well as the relationship to use cases
EO 5.2
Master and use simple scenario modeling with sequence diagrams
EO 5.3
Master and use advanced scenario modeling with sequence diagrams
EO 5.4
Master and use scenario modeling with communication diagrams
Prerequisite: Basic views of requirements modeling (foundation level), use case diagrams,
use case specifications
Topic overview: In requirements engineering, scenarios describe sequences of messages
between the system to be developed and actors in the system context. These sequences
lead to the goals of one or more actors being achieved, in other words, the use of the system
provides a desired added value for actors. In both conventional requirements engineering as
well as agile development processes, scenarios document the central requirements of the
behavior in respect of the use of the system under consideration. They do so, for example, in
the form of main, alternative, and exception scenarios or in the form of user stories. The aim
of this educational unit is to build up the theoretical and practical knowledge required for
documenting scenarios in the form of diagrams. Modeled scenarios have a higher level of
formalization in comparison to textual documentation. This produces clearer, more
understandable, and more precise scenario descriptions — even if the usage behavior of the
system is very complex. Furthermore, modeled scenarios have clear advantages in terms of
automatic analysis and the ability to be integrated with other requirements models, as well as
in relation to the automatic derivation of further development artifacts (e.g., test cases for
the system test). This educational unit focuses on documenting scenarios using UML
sequence diagrams. It also looks at scenario modeling with communication diagrams. For
both types of diagrams, the unit covers the syntax and semantics of the different modeling
constructs and the integration of modeled scenarios with other diagrams from requirements
modeling. Furthermore, the unit offers heuristics that make it easier for you to start modeling
scenarios.
Literature reference: Chapter 5, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-requirements-
modeling





Requirements Modeling | Syllabus | © IREB
24 | 26
5.1 Basic principles of scenario modeling in requirements
engineering (L3)
Duration: 15 minutes (theory)
Content: In this educational unit you become familiar with the purpose of scenario modeling
in requirements engineering. One aim of the unit is to convey the importance of scenarios in
requirements engineering. Scenarios are used to document example usage sequences
between the system under consideration and the actors in context at the interface of the
system under consideration to its context. The unit also introduces the different forms of
representation for scenarios (narrative text, structured text, diagram) and the link between
scenarios and use case. It also gives an overview of the different approaches for scenario
modeling, such as the ITU Message Sequence Charts (MSCs) and UML sequence diagrams
and communication diagrams.
5.2 Simple scenario modeling with sequence diagrams (L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: In this educational unit you learn how to model simple scenarios using UML
sequence diagrams. You become familiar with the syntax and semantics of the different
basic modeling constructs of sequence diagrams for scenario modeling in requirements
engineering, as well as rules and tips for modeling simple scenarios. You learn how to model
interaction frames and lifelines for the system under consideration and the actors in the
system context. The unit also explains the importance and modeling of the following: the
activation of instances in scenarios; the termination of lifelines; and asynchronous and
synchronous messages in scenario modeling (using sequence diagrams). This unit looks at
the relationships of scenario modeling in requirements engineering to context modeling and
use case modeling. It also discusses the relationships of messages in scenarios to the
modeling of requirements in the state-oriented view, the data flow-oriented view, and the
information structure view in requirements modeling.





Requirements Modeling | Syllabus | © IREB
25 | 26
5.3 Advanced scenario modeling with sequence diagrams (L3)
Duration: 30 minutes (theory); 30 minutes (exercises)
Content: This educational unit looks at advanced scenario modeling using sequence
diagrams. You become familiar with the syntax and semantics of the different advanced
modeling constructs of sequence diagrams for scenario modeling in requirements
engineering. The unit also offers rules and tips for advanced scenario modeling. You become
familiar with using combined fragments to model alternative interactions in scenarios ("alt")
as well as optional interactions ("opt"). You also learn how to abstract from interactions
within complex scenarios by modeling the abstracted interactions in a separate sequence
diagram and, in the original scenario, referring to the "outsourced" (abstracted) partial
scenario using the combined fragment ("ref"). Furthermore, you learn how to model
repetitions ("loop") of interactions linked to boolean conditions as well as how to model
exception handling ("break") in scenarios. The unit also addresses the modeling of
assumptions for scenarios and nesting combined fragments in scenario modeling.
5.4 Scenario modeling with communication diagrams (L3)
Duration: 15 minutes (theory); 15 minutes (exercises)
Content: In this educational unit you learn how to model simple scenarios using UML
communication diagrams. You become familiar with the syntax and semantics of the
different modeling constructs of communication diagrams for scenario modeling in
requirements engineering. The unit also offers rules and tips for modeling simple scenarios
with UML communication diagrams. It focuses on the different representation of scenarios
compared to scenario modeling with sequence diagrams. Scenario modeling with sequence
diagrams concentrates on the order in which messages are exchanged, whereas in scenario
modeling with communication diagrams, it is the interfaces of the system to actors in the
system context that is the focus. This is why, when communication diagrams are used, the
individual interfaces and the message exchange at these interfaces is visualized.





Requirements Modeling | Syllabus | © IREB
26 | 26
Glossary
See chapter 6, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-requirements-
modeling.
Literature
Primary literature: Cziharz, T.; Hruschka, P.; Queins, S.; Weyer, T.: Handbook of
Requirements Modeling IREB Standard – Education and training for IREB
Certified Professional for Requirements Requirements Modeling,
International Requirements Engineering Board, Karlsruhe, available online
at: https://www.ireb.org/en/downloads/#handbook-cpre-advanced-
level-requirements-modeling
References:
See chapter 8, Handbook Requirements Modeling,
https://www.ireb.org/en/downloads/#handbook-cpre-advanced-level-
requirements-modeling.
