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
            operates_on_particles = cms.vint32(511),
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
Decay myMuTau+
0.17400     mu+ nu_mu anti-nu_tau                       PHOTOS  TAULNUNU;  #[Reconstructed PDG2011]
Enddecay
#
#
Alias myLepD_s+ D_s+
Decay myLepD_s+
0.02400     eta     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.01900     phi     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.01100     eta'    mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00550     mu+     nu_mu                                   PHOTOS  SLN;   #[Reconstructed PDG2011]
0.00950     myMuTau+    nu_tau                                      SLN;   #[Reconstructed PDG2011] 0.055 * 0.174
Enddecay
#
#
#
Alias myLepD_s*+ D_s*+
Decay myLepD_s*+
0.942000000 myLepD_s+    gamma                                   VSP_PWAVE; #[Reconstructed PDG2011]
0.058000000 myLepD_s+    pi0                                     VSS; #[Reconstructed PDG2011]
Enddecay
#
#
#
Alias myLepD_s0*+ D_s0*+
Decay myLepD_s0*+
1.000      myLepD_s+ pi0                        PHSP;
Enddecay
#
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
##########################################
#           B0 -> D*- Ds(*)
##########################################
#
Decay B0
0.00800     MyD*-         myLepD_s+                                 SVS; #[Reconstructed PDG2011]
0.01770     myLepD_s*+    MyD*-                                     SVV_HELAMP 0.4904 0.0 0.7204 0.0 0.4904 0.0; #[Reconstructed PDG2011]
0.00150     MyD*-         myLepD_s0*+                               SVS;
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
        processParameters = cms.vstring('HardQCD:hardbbbar = on'),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
mufilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13)
)

DstFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-413),
    MotherID           = cms.untracked.int32(511),
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-421, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.2),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

antiD0Filter = cms.EDFilter(
    "PythiaDauVFilter",
    ChargeConjugation  = cms.untracked.bool(False),
    ParticleID         = cms.untracked.int32(-421),
    MotherID           = cms.untracked.int32(-413),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(321, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.5),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

ProductionFilterSequence = cms.Sequence(generator + mufilter + DstFilter + antiD0Filter)
