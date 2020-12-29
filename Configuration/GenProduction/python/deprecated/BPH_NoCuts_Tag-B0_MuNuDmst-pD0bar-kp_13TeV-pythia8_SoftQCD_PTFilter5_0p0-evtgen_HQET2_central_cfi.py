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
            # list_forced_decays = cms.vstring('B+','B-'),
            # operates_on_particles = cms.vint32(521),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#from EX: https://hflav-eos.web.cern.ch/hflav-eos/semi/summer16/html/ExclusiveVcb/exclBtoDstar.html
Define rho2 1.205 #pm 0.026
#Define etaEW-F1-Vcb 0.0356 #pm 0.0004
Define R1_1 1.404 #pm 0.032
Define R2_1 0.854 #pm 0.020
#R0_1 (helicity suppressed ff) from TH: https://journals.aps.org/prd/pdf/10.1103/PhysRevD.85.094025
Define R0_1 1.14 #pm 10%
#hA1_1 (ff norm) from TH: https://journals.aps.org/prd/pdf/10.1103/PhysRevD.79.014506
Define hA1_1 0.921 #pm 0.024
#
Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj MyD0   Myanti-D0
#
Decay MyD0
1.000      K-  pi+                PHSP;
Enddecay
CDecay Myanti-D0
#
#
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
Decay B0
1.000     MyD*- mu+ nu_mu         PHOTOS  HQET2 rho2 hA1_1 R1_1 R2_1 R0_1;
Enddecay
#
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
                                        'SoftQCD:nonDiffractive = on',
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
tagfilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(511),  ## B0
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(3),
    DaughterIDs        = cms.untracked.vint32(-413, -13, 14),
    MinPt              = cms.untracked.vdouble(-1., -1, -1.),
    MinEta             = cms.untracked.vdouble(-9999999., -9999999., -9999999.),
    MaxEta             = cms.untracked.vdouble( 9999999.,  9999999., 9999999.)
)


ProductionFilterSequence = cms.Sequence(generator + tagfilter)
