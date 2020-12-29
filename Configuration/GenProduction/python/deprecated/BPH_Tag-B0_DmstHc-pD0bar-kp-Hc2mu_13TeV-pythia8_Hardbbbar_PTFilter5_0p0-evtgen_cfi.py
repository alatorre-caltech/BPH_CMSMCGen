import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for the decay B0 -> Dst Hc (-> mu)
#
yesPhotos
##########################################
#           Hc -> mu
##########################################
#
Alias myMuTau+ tau+
Alias myMuTau- tau-
ChargeConj myMuTau+ myMuTau-
Decay myMuTau-
0.170000000 mu-     anti-nu_mu nu_tau                       PHOTOS  TAULNUNU; #[Reconstructed PDG2011]
0.003900000 mu-     anti-nu_mu nu_tau  gamma                PHSP;  #[New mode added] #[Reconstructed PDG2011]
Enddecay
## Tot BR = 0.1739
CDecay myMuTau+
#
Alias myLepD_s+ D_s+
Alias myLepD_s- D_s-
ChargeConj myLepD_s+ myLepD_s-
Decay myLepD_s+
0.018309605 phi     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.022845082 eta     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.008186726 eta'    mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.002058115 anti-K0 mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.000762265 anti-K*0 mu+     nu_mu                          PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.005800000 mu+     nu_mu                                   PHOTOS  SLN; #[Reconstructed PDG2011]
0.005398960 myMuTau+    nu_tau                                  SLN; #[Reconstructed PDG2011] 0.0311* 0.1736
Enddecay
## Tot BR = 0.063360753
CDecay myLepD_s-
#
Alias myLepD_s*+ D_s*+
Alias myLepD_s*- D_s*-
ChargeConj myLepD_s*- myLepD_s*+
Decay myLepD_s*+
0.942000000 myLepD_s+    gamma                                   VSP_PWAVE; #[Reconstructed PDG2011]
0.058000000 myLepD_s+    pi0                                     VSS; #[Reconstructed PDG2011]
Enddecay
## Tot BR = 0.063360753
CDecay myLepD_s*-
#
Alias myLepD+ D+
Alias myLepD- D-
ChargeConj myLepD- myLepD+
Decay myLepD+
0.052800000 anti-K*0 mu+     nu_mu                          PHOTOS  ISGW2; # PDG2014
0.092000000 anti-K0 mu+     nu_mu                           PHOTOS  ISGW2; # PDG2014
0.002773020 anti-K_10 mu+     nu_mu                         PHOTOS  ISGW2; # Keep same as in 2010 version
0.002927076 anti-K_2*0 mu+     nu_mu                        PHOTOS  ISGW2; # Keep same as in 2010 version
0.004050000 pi0     mu+     nu_mu                           PHOTOS  ISGW2; # Same as electron
0.001140000 eta     mu+     nu_mu                           PHOTOS  ISGW2; # Same as electron
0.002200000 eta'    mu+     nu_mu                           PHOTOS  ISGW2; # Same as electron
0.002400000 rho0    mu+     nu_mu                           PHOTOS  ISGW2; # PDG2014
0.001820000 omega   mu+     nu_mu                           PHOTOS  ISGW2; # Same as electron
0.002921725 K-      pi+     mu+     nu_mu                   PHOTOS   PHSP; # PDG2014 (subtracted K*)+tiny bit to have sum=1
0.001200122 anti-K0 pi0     mu+     nu_mu                   PHOTOS   PHSP; # Keep same as in 2010 version+tiny bit to have sum=1
0.000382000 mu+     nu_mu                                   PHOTOS   SLN; #[Reconstructed PDG2011]
Enddecay
## Tot BR = 0.166613943
CDecay myLepD-
#
Alias myLepD0 D0
Alias myLepanti-D0 anti-D0
ChargeConj myLepanti-D0 myLepD0
Decay myLepD0
0.021000000 K*-     mu+     nu_mu                           PHOTOS  ISGW2; # 1.1 * PDG2014
0.034700000 K-      mu+     nu_mu                           PHOTOS  ISGW2; # 1.05 * PDG2014
0.000076000 K_1-    mu+     nu_mu                           PHOTOS  ISGW2; # PDG2014 for electron
0.001100000 K_2*-   mu+     nu_mu                           PHOTOS  ISGW2; # copy from electron
0.002370000 pi-     mu+     nu_mu                           PHOTOS  ISGW2; # PDG2014
0.002015940 rho-    mu+     nu_mu                           PHOTOS  ISGW2; # PDG2014 for electron
0.001080000 anti-K0 pi-     mu+     nu_mu                   PHOTOS   PHSP; # copy electron
Enddecay
## Tot BR = 0.06234194
CDecay myLepanti-D0
#
Alias myLepD*+ D*+
Decay myLepD*+
0.2533    myLepD0  pi+                        VSS;  #0.6770*0.06234194/0.166613943
0.3070    myLepD+  pi0                        VSS;
0.0160    myLepD+  gamma                       VSP_PWAVE;
Enddecay
## Tot BR = 0.166613943
#
Alias myLepD*0 D*0
Alias myLepanti-D*0 anti-D*0
ChargeConj myLepanti-D*0 myLepD*0
Decay myLepD*0
0.619000000 myLepD0      pi0                                     VSS; #[Reconstructed PDG2011]
0.381000000 myLepD0      gamma                                   VSP_PWAVE; #[Reconstructed PDG2011]
Enddecay
CDecay myLepanti-D*0
## Tot BR = 0.06234194
#
Alias myLepD_s0*+ D_s0*+
Alias myLepD_s0*- D_s0*-
ChargeConj myLepD_s0*- myLepD_s0*+
Decay myLepD_s0*+
1.000      myLepD_s+ pi0                        PHSP;
Enddecay
CDecay myLepD_s0*-
## Tot BR = 0.063360753
#
Alias myLepD_s1+ D_s1+
Alias myLepD_s1- D_s1-
ChargeConj myLepD_s1- myLepD_s1+
Decay myLepD_s1+
0.80000  myLepD_s*+ pi0                       PARTWAVE 1.0 0.0 0.0 0.0 0.0 0.0;
0.20000  myLepD_s+ gamma                       VSP_PWAVE;
Enddecay
CDecay myLepD_s1-
## Tot BR = 0.063360753
#
#
#
#
#
##########################################
#           D*- -> D0(->Kpi) pi
##########################################
#
Alias      Myanti-D0   anti-D0
Decay Myanti-D0
1.000      K+  pi-                PHSP;
Enddecay
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
#
#
Alias myD'_1- D'_1-
Decay myD'_1-
0.3333    MyD*- pi0                        VVS_PWAVE  1.0 0.0 0.0 0.0 0.0 0.0;
Enddecay
#
Alias myD_1- D_1-
Decay myD_1-
0.3333    MyD*- pi0                        VVS_PWAVE  0.0 0.0 0.0 0.0 1.0 0.0;
Enddecay
#
Alias myD_2*- D_2*-
Decay myD_2*-
0.1030    MyD*- pi0                        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
#
#
#
#
Decay B0
### All channels will be normalized to the D*- D_s+ () BR
0.000802030 MyD*-         myLepD+              SVS; #  0.000305 *0.166613943/0.063360753
# 0.000610000 D*+     D-                                      SVS; #[Reconstructed PDG2011]         -- Negative muon sign
0.00215627  MyD*-         myLepD*+                                     SVV_HELAMP 0.56 0.0 0.96 0.0 0.47 0.0; #[Reconstructed PDG2011]  0.00082000*0.166613943/0.063360753
0.008000000 MyD*-         myLepD_s+                                    SVS; #[Reconstructed PDG2011] # *1
0.017700000 myLepD_s*+    MyD*-                                     SVV_HELAMP 0.4904 0.0 0.7204 0.0 0.4904 0.0; #[Reconstructed PDG2011] # *1
0.0002      myD'_1-       myLepD_s+                SVS; # 0.0006 * 0.3333
0.0004      myD'_1-       myLepD_s*+              SVV_HELAMP 0.48 0.0 0.734 0.0 0.48 0.0; #0.0012*0.333
0.0004      myD_1-        myLepD_s+                SVS;#0.0012*0.333
0.0008      myD_1-        myLepD_s*+               SVV_HELAMP 0.48 0.0 0.734 0.0 0.48 0.0; #0.0024*0.333
0.0004      myD_2*-       myLepD_s+                      STS; # 0.004*0.1
0.0004      myD_2*-       myLepD_s*+                    PHSP; # 0.004*0.1
0.003100000 MyD*-         myLepD0         K+                              PHSP; #[Reconstructed PDG2011] # *0.06234194/0.063360753 ~ 1
0.011800000 MyD*-         myLepD*0        K+                              PHSP; #[Reconstructed PDG2011] # *0.06234194/0.063360753 ~ 1
0.0018      MyD*-         myLepD+         K0                         PHSP;
# 0.0047   D-  D*+  K0                        PHSP;         -- Negative muon sign
0.0205      MyD*-         myLepD*+        K0                              PHSP; #[Reconstructed PDG2011]   #  0.0078*0.166613943/0.063360753
0.0025      MyD*-         myLepD0         K*+                        PHSP; # *0.06234194/0.063360753 ~ 1
0.0050      MyD*-         myLepD*0        K*+                       PHSP; # *0.06234194/0.063360753 ~ 1
0.0025      MyD*-         myLepD+         K*0                        PHSP;
0.0131      MyD*-         myLepD*+        K*0                       PHSP;   #  0.0050*0.166613943/0.063360753
# 0.0016      D_s0*+      D-                                      PHSP;         -- Negative muon sign
0.0015      MyD*-         myLepD_s0*+                                  SVS;  #*1
# 0.003500000 D_s1+       D-                                      SVS; #[Reconstructed PDG2011]         -- Negative muon sign
0.009300000 MyD*-         myLepD_s1+                                   SVV_HELAMP 0.4904 0. 0.7204 0. 0.4904 0.; #[Reconstructed PDG2011]  #*1
# 0.00043     D'_s1+      D-                                      PHSP;         -- Neglected
# 0.00083     D'_s1+      D*-                                     PHSP;         -- Neglected
Enddecay
End
"""
                                            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
                                        'HardQCD:hardbbbar = on',
                    					'PTFilter:filter = on',
                                        'PTFilter:quarkToFilter = 5',
                                        'PTFilter:scaleToFilter = 1.0',
                                        'PTFilter:quarkPt = 0.0'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
mufilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(6.5),
    ParticleID = cms.untracked.int32(13),
)

DstFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-413),
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-421, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.5),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

antiD0Filter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-421),
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(321, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.5),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

ProductionFilterSequence = cms.Sequence(generator + mufilter + DstFilter + antiD0Filter)
